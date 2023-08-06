import logging
from util.datetime_util import DATE_FORMAT

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT, datefmt=DATE_FORMAT)
log = logging
