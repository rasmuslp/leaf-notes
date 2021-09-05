"""Command Line Interface"""

import argparse
import logging
from string import Template

from notes.note import Note
from notes.weather import Weather

logger = logging.getLogger(__name__)


def run(args):
    """Runner"""
    logger.debug('Running')
    weather = Weather()
    forecast = weather.getForecast(args.weather_latitude[0], args.weather_longitude[0], args.weather_altitude[0])

    print(forecast)

    note = Note()
    note.update({
        'quoteTitle': 'BE LIGHT',
        'quoteText': 'If you are happy, happiness will come to you because happiness wants to go where happiness is.',
        'quoteAuthor': '- Yogi Bhajan',
        'weatherIcon': './notes/01d.png',
        'weatherTemperature': Template('${temperature} C').substitute(temperature=forecast['now']['airTemperature']),
        'weatherWindSpeed': Template('${speed} m/s').substitute(speed=forecast['now']['windSpeed']),
        'weatherWindDirection': Template('${direction}').substitute(direction=forecast['now']['windFromDirection']),
        'weatherPrecipitation': Template('${precipitation} mm').substitute(precipitation=forecast['next6Hours']['precipitationAmount'])

    })
    note.write('./img.bmp')


def cli():
    """CLI definition and execution"""
    programParser = argparse.ArgumentParser(description='Generates leaf-note as images',
                                            allow_abbrev=False)

    group = programParser.add_mutually_exclusive_group()
    group.add_argument('-v',
                       '--verbose',
                       action='store_true',
                       help='increase output verbosity')
    group.add_argument('-q',
                       '--quiet',
                       action='store_true',
                       help='decrease verbosity to absolute minimum')

    programParser.add_argument('--weather-latitude',
                               nargs=1,
                               required=True,
                               type=float,
                               metavar='degrees',
                               help='Latitude for weather information')

    programParser.add_argument('--weather-longitude',
                               nargs=1,
                               required=True,
                               type=float,
                               metavar='degrees',
                               help='Longitude for weather information')

    programParser.add_argument('--weather-altitude',
                               nargs=1,
                               required=True,
                               type=int,
                               metavar='height',
                               help='Height above sea level in meters')

    args = programParser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    elif args.quiet:
        logging.basicConfig(level=logging.WARNING)

    logger.debug('Parsed arguments %s', args)
    run(args)
