"""Command Line Interface"""

import argparse
import logging
import random
from string import Template
import subprocess
import sys

from common.cli_helpers import addVerboseAndQuiet, unfoldArgValueIfArrayOneFrom
from common.env_default import envDefault
from notes.note import Note
from notes.quote import loadQuotes
from notes.weather import Weather

logger = logging.getLogger(__name__)


def run(args):
    """Runner"""
    logger.debug('Running')
    quotes = loadQuotes(args.quotes_path)
    randomQuote = random.choice(quotes)

    weather = Weather()
    forecast = weather.getForecast(args.weather_latitude, args.weather_longitude, args.weather_altitude)

    print(forecast)

    note = Note()
    note.update({
        'quoteTitle': randomQuote.title,
        'quoteText': randomQuote.quote,
        'quoteAuthor': Template('- ${author}').substitute(author=randomQuote.author),
        'weatherIcon': Template('./notes/metno-icons/png/${icon}.png').substitute(icon=forecast['next6Hours']['symbolCode']),
        'weatherTemperature': Template('${temperature} C').substitute(temperature=forecast['now']['airTemperature']),
        'weatherWindSpeed': Template('${speed} m/s').substitute(speed=forecast['now']['windSpeed']),
        'weatherWindDirection': Template('${direction}').substitute(direction=forecast['now']['windFromDirection']),
        'weatherPrecipitation': Template('${precipitation} mm').substitute(precipitation=forecast['next6Hours']['precipitationAmount'])

    })
    note.write('./img-black.bmp', './img-colour.bmp')

    if args.update_display:
        try:
            subprocess.run(['python', '-m', 'display', 'render', '-b', './img-black.bmp', '-c', './img-colour.bmp', '-r', str(args.rotate)], check=True)
        except subprocess.CalledProcessError as exc:
            logger.error('Err running \'display\', see above for details. %s', exc)
            sys.exit(1)


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

    logger.debug('Parsed arguments %s', args)
    run(args)
