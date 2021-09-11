"""Command Line Interface"""

import argparse
import logging
import time
import schedule

from common.cli_helpers import addVerboseAndQuiet, unfoldArgValueIfArrayOneFrom
from common.env_default import envDefault
from notes.runner import Runner

logger = logging.getLogger(__name__)


def cli():
    """CLI definition and execution"""
    programParser = argparse.ArgumentParser(description='Generates leaf-note as images',
                                            allow_abbrev=False)

    verboseAndQuietGroup = programParser.add_mutually_exclusive_group()
    addVerboseAndQuiet(verboseAndQuietGroup)

    programParser.add_argument('--quotes-path',
                               nargs=1,
                               action=envDefault('QUOTES_PATH'),
                               required=True,
                               metavar='path',
                               help='Path to yaml file with Quote definitions')

    programParser.add_argument('--weather-latitude',
                               nargs=1,
                               action=envDefault('WEATHER_LATITUDE'),
                               required=True,
                               type=float,
                               metavar='degrees',
                               help='Latitude for weather information')

    programParser.add_argument('--weather-longitude',
                               nargs=1,
                               action=envDefault('WEATHER_LONGITUDE'),
                               required=True,
                               type=float,
                               metavar='degrees',
                               help='Longitude for weather information')

    programParser.add_argument('--weather-altitude',
                               nargs=1,
                               action=envDefault('WEATHER_ALTITUDE'),
                               required=True,
                               type=int,
                               metavar='height',
                               help='Height above sea level in meters')

    programParser.add_argument('-u',
                               '--update-display',
                               action=envDefault('UPDATE_DISPLAY'),
                               subAction='store_true',
                               help='Invoke display module to also update the display')

    programParser.add_argument('-r',
                               '--rotate',
                               action=envDefault('ROTATE'),
                               default=0,
                               nargs=1,
                               type=int,
                               metavar='degrees',
                               help='Rotate image a number of degrees, defaults to 0')

    args = vars(programParser.parse_args())
    argsToUnfold = [
        'quotes_path',
        'weather_latitude',
        'weather_longitude',
        'weather_altitude',
        'rotate'
    ]
    args = unfoldArgValueIfArrayOneFrom(args, argsToUnfold)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    elif args.quiet:
        logging.basicConfig(level=logging.WARNING)
    else:
        logging.basicConfig(level=logging.INFO)

    logger.debug('Parsed arguments %s', args)
    runner = Runner(**vars(args))
    schedule.every().hour.at(':00').do(runner.run)
    schedule.run_all()

    while True:
        schedule.run_pending()
        time.sleep(60)
