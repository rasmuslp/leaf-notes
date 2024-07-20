"""Global logger configuration"""

import logging

LOGGER_FORMAT = '%(asctime)s %(levelname)s [%(name)s] {%(module)s} [%(funcName)s] %(message)s'

logging.basicConfig(level=logging.INFO, format=LOGGER_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')


def setVerboseOrQuiet(verbose, quiet):
    """Set log level globally to verbose or quiet"""
    if verbose:
        logging.root.setLevel(logging.DEBUG)
    elif quiet:
        logging.root.setLevel(logging.WARNING)
