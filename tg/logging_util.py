from datetime import datetime
from pytz import timezone
import logging
import sys


def timetz(*args):
    return datetime.now(tz).timetuple()


tz = timezone('America/Los_Angeles')
logging.Formatter.converter = timetz
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

logging = logging
