import logging
from threading import Thread
from multiprocessing.pool import Pool
import monotonic
import backoff
import json

from analytics.version import VERSION
from analytics.request import post, APIError, DatetimeSerializer

try:
    from queue import Empty
except ImportError:
    from Queue import Empty

MAX_MSG_SIZE = 32 << 10

# Our servers only accept batches less than 500KB. Here limit is set slightly
# lower to leave space for extra data that will be added later, eg. "sentAt".
BATCH_SIZE_LIMIT = 475000


def request(batch, write_key, host, gzip, timeout, retries):
    """Attempt to upload the batch and retry before raising an error """

    def fatal_exception(exc):
        if isinstance(exc, APIError):
            # retry on server errors and client errors with 429 status code (rate limited),
            # don't retry on other client errors
            return (400 <= exc.status < 500) and exc.status != 429
        else:
            # retry on all other errors (eg. network)
            return False

    @backoff.on_exception(backoff.expo, Exception, max_tries=retries + 1, giveup=fatal_exception)
    def send_request():
        post(write_key, host, gzip=gzip, timeout=timeout, batch=batch)

    send_request()


class Consumer(Thread):
    """Consumes the messages from the client's queue."""
    log = logging.getLogger('segment')

    def __init__(self, queue, write_key, upload_size=100, host=None, on_error=None,
                 upload_interval=0.5, gzip=False, retries=10, timeout=15):
        """Create a consumer thread."""
        Thread.__init__(self)
        # Make consumer a daemon thread so that it doesn't block program exit
        self.daemon = True
        self.upload_size = upload_size
        self.upload_interval = upload_interval
        self.write_key = write_key
        self.host = host
        self.on_error = on_error
        self.queue = queue
        self.gzip = gzip
        # It's important to set running in the constructor: if we are asked to
        # pause immediately after construction, we might set running to True in
        # run() *after* we set it to False in pause... and keep running forever.
        self.running = True
        self.retries = retries
        self.timeout = timeout
        self.pool = Pool(32)

    def run(self):
        """Runs the consumer."""
        self.log.debug('consumer is running...')
        while self.running:
            self.upload()

        self.pool.close()
        self.pool.join()
        self.log.debug('consumer exited.')

    def pause(self):
        """Pause the consumer."""
        self.running = False

    def upload(self):
        """Asynchronously upload the next batch of items."""
        batch = self.next()
        length = len(batch)
        if length == 0:
            return

        def on_success(x):
            done()

        def on_error(e):
            self.log.error('error uploading: %s', e)
            if self.on_error:
                self.on_error(e, batch)
            done()

        def done():
            for i in range(length):
                self.queue.task_done()

        self.pool.apply_async(
            request,
            args=[batch, self.write_key, self.host, self.gzip, self.timeout, self.retries],
            callback=on_success,
            error_callback=on_error
        )

    def next(self):
        """Return the next batch of items to upload."""
        queue = self.queue
        items = []

        start_time = monotonic.monotonic()
        total_size = 0

        while len(items) < self.upload_size:
            elapsed = monotonic.monotonic() - start_time
            if elapsed >= self.upload_interval:
                break
            try:
                item = queue.get(block=True, timeout=self.upload_interval - elapsed)
                item_size = len(json.dumps(item, cls=DatetimeSerializer).encode())
                if item_size > MAX_MSG_SIZE:
                    self.log.error('Item exceeds 32kb limit, dropping. (%s)', str(item))
                    continue
                items.append(item)
                total_size += item_size
                if total_size >= BATCH_SIZE_LIMIT:
                    self.log.debug('hit batch size limit (size: %d)', total_size)
                    break
            except Empty:
                break

        return items
