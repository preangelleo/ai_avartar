from datetime import datetime
from pytz import timezone
import logging
import time

from src.utils.metrics import FUNCTION_CALL_LATENCY_METRICS


def timetz(*args):
    return datetime.now(tz).timetuple()


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        # TODO: configure statsd to monitor execution time and integrate with cloudwatch
        start_time = time.time()

        # Execute the function
        result = func(*args, **kwargs)

        FUNCTION_CALL_LATENCY_METRICS.labels(func.__name__).observe(time.time() - start_time)

        return result

    return wrapper


tz = timezone('America/Los_Angeles')
logging.Formatter.converter = timetz
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)

logging = logging
