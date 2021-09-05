"""Command Line Interface"""

import argparse
import logging
import random
from string import Template
import subprocess

from notes.note import Note
from notes.quote import loadQuotes
from notes.weather import Weather

logger = logging.getLogger(__name__)


def run(args):
    """Runner"""
    logger.debug('Running')
    quotes = loadQuotes(args.quotes[0])
    randomQuote = random.choice(quotes)

    weather = Weather()
    forecast = weather.getForecast(args.weather_latitude[0], args.weather_longitude[0], args.weather_altitude[0])

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
        subprocess.run(['.venv/bin/python', '-m', 'display', '-v', 'render', '-b', './img-black.bmp', '-c', './img-colour.bmp', '-r', args.rotate[0]], check=True)


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

    programParser.add_argument('--quotes',
                               nargs=1,
                               required=True,
                               metavar='path',
                               help='Path to yaml file with Quote definitions')

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

    programParser.add_argument('-u',
                               '--update-display',
                               action='store_true',
                               help='Invoke display module to also update the display')

    programParser.add_argument('-r',
                               '--rotate',
                               default=0,
                               nargs=1,
                               type=int,
                               metavar='degrees',
                               help='Rotate image a number of degrees, defaults to 0')

    args = programParser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    elif args.quiet:
        logging.basicConfig(level=logging.WARNING)

    logger.debug('Parsed arguments %s', args)
    run(args)
