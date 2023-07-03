from datetime import datetime
from pytz import timezone
import logging
import time

# from statsd import StatsClient


def timetz(*args):
    return datetime.now(tz).timetuple()


# Initialize StatsD client
# statsd_client = StatsClient(host='localhost', port=8125, prefix='MyApplication')


def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        # TODO: configure statsd to monitor execution time and integrate with cloudwatch
        start_time = time.time()

        # Execute the function
        result = func(*args, **kwargs)

        # Measure execution time
        execution_time = time.time() - start_time

        # Send execution time to CloudWatch via StatsD
        # statsd_client.timing('FunctionExecutionTime', execution_time)
        logging.info(f'Function {func.__name__} executed in {execution_time} seconds')

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
