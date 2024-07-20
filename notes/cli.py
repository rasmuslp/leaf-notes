"""Command Line Interface"""

import argparse
import logging

from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from common.cli_helpers import addVerboseAndQuiet, unfoldArgValueIfArrayOneFrom
from common.env_default import envDefault
from common.logger import setVerboseOrQuiet
from notes.runner import Runner

logger = logging.getLogger(__name__)


def cli():
    """CLI definition and execution"""
    programParser = argparse.ArgumentParser(description='Generates leaf-note as images', allow_abbrev=False)

    verboseAndQuietGroup = programParser.add_mutually_exclusive_group()
    addVerboseAndQuiet(verboseAndQuietGroup)

    programParser.add_argument(
        '--cron-schedule',
        nargs=1,
        action=envDefault('CRON_SCHEDULE'),
        default='0 * * * *',
        metavar='schedule',
        help='Cron expression that determines the interval of this, defaults to hourly on minute 0',
    )

    programParser.add_argument(
        '--quotes-path',
        nargs=1,
        action=envDefault('QUOTES_PATH'),
        required=True,
        metavar='path',
        help='Path to yaml file with Quote definitions',
    )

    programParser.add_argument(
        '--weather-latitude',
        nargs=1,
        action=envDefault('WEATHER_LATITUDE'),
        required=True,
        type=float,
        metavar='degrees',
        help='Latitude for weather information',
    )

    programParser.add_argument(
        '--weather-longitude',
        nargs=1,
        action=envDefault('WEATHER_LONGITUDE'),
        required=True,
        type=float,
        metavar='degrees',
        help='Longitude for weather information',
    )

    programParser.add_argument(
        '--weather-altitude',
        nargs=1,
        action=envDefault('WEATHER_ALTITUDE'),
        required=True,
        type=int,
        metavar='height',
        help='Height above sea level in meters',
    )

    programParser.add_argument(
        '-u',
        '--update-display',
        action=envDefault('UPDATE_DISPLAY'),
        subAction='store_true',
        help='Invoke display module to also update the display',
    )

    programParser.add_argument(
        '-r',
        '--rotate',
        action=envDefault('ROTATE'),
        default=0,
        nargs=1,
        type=int,
        metavar='degrees',
        help='Rotate image a number of degrees, defaults to 0',
    )

    args = vars(programParser.parse_args())
    argsToUnfold = [
        'cron_schedule',
        'quotes_path',
        'weather_latitude',
        'weather_longitude',
        'weather_altitude',
        'rotate',
    ]
    args = unfoldArgValueIfArrayOneFrom(args, argsToUnfold)

    setVerboseOrQuiet(args.verbose, args.quiet)

    logger.debug('Parsed arguments %s', args)

    runner = Runner(
        verbose=args.verbose,
        quiet=args.quiet,
        quotesPath=args.quotes_path,
        weatherLatitude=args.weather_latitude,
        weatherLongitude=args.weather_longitude,
        weatherAltitude=args.weather_altitude,
        updateDisplay=args.update_display,
        rotate=args.rotate,
    )
    runner.run()

    scheduler = BlockingScheduler()
    cronTrigger = CronTrigger.from_crontab(args.cron_schedule)
    scheduler.add_job(runner.run, trigger=cronTrigger, max_instances=1)
    scheduler.start()
