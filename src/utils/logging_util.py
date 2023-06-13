from datetime import datetime
from pytz import timezone
import logging


def timetz(*args):
    return datetime.now(tz).timetuple()


tz = timezone('America/Los_Angeles')
logging.Formatter.converter = timetz
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)

logging = logging
