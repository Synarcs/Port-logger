"""Usage: tcp_logger [-hso FILE] [--quiet | --verbose] [INPUT ...]

tcp_logger
A simple Tcp Port Logger

Usage:
   tcp_logger --config File

Options:
    --config Path to ports config File
    -h --help    A simple Tcp logger when a port is connected
    --quiet      logger.info __quiet text
    --verbose   logger.info the Verbose Text

"""

from docopt import docopt
from configparser import ConfigParser
from tcp_logger import HoneyPot
from sys import exit
import logging

config = ConfigParser()
config_path = 'config_data.ini'
config.read('config_data.ini')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
PortFile = config.get("default", "ports", raw=True,
                      fallback="23,22,21,443,80,8080")
logging_file = config.get("default", "logFile", raw=True, fallback='config_data.ini')

logger.info('the logFile is {}'.format(logging_file))
logger.info('the ports file is {}'.format(PortFile))


PortFile = PortFile.split(',')
try:
    print(__name__)
    Honey = HoneyPot(PortFile, logging_file)
    Honey.run()
except:
    logger.info('eroor in port configured')
    exit(1)
