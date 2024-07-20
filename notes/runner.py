"""Runner that holds references and can run the core logic"""

import logging
import random
from string import Template
import subprocess
import sys

from notes.note import Note
from notes.quote import loadQuotes
from notes.weather import Weather

logger = logging.getLogger(__name__)


class Runner:
    """Runner that keeps the state of the core logic"""

    # pylint: disable=too-many-arguments,too-many-instance-attributes
    def __init__(
        self,
        verbose=False,
        quiet=False,
        quotesPath=None,
        weatherLatitude=None,
        weatherLongitude=None,
        weatherAltitude=None,
        updateDisplay=False,
        rotate=None,
    ) -> None:
        self.verbose = verbose
        self.quiet = quiet
        self.quotes = loadQuotes(quotesPath)
        self.weather = Weather()
        self.weatherLatitude = weatherLatitude
        self.weatherLongitude = weatherLongitude
        self.weatherAltitude = weatherAltitude
        self.note = Note()
        self.updateDisplay = updateDisplay
        self.rotate = rotate

    def run(self):
        """Run the core logic"""
        logger.info('Run')

        randomQuote = random.choice(self.quotes)
        logger.debug('Random quote %s', randomQuote)

        logger.info('Getting forecast')
        forecast = self.weather.getForecast(self.weatherLatitude, self.weatherLongitude, self.weatherAltitude)
        logger.debug('Forecast %s', forecast)

        logger.debug('Generating note')
        self.note.update(
            {
                'quoteTitle': randomQuote.title,
                'quoteText': randomQuote.quote,
                'quoteAuthor': Template('- ${author}').substitute(author=randomQuote.author),
                'weatherIcon': Template('./notes/metno-icons/png/${icon}.png').substitute(
                    icon=forecast['next6Hours']['symbolCode']
                ),
                'weatherTemperature': Template('${temperature} C').substitute(
                    temperature=forecast['now']['airTemperature']
                ),
                'weatherWindSpeed': Template('${speed} m/s').substitute(speed=forecast['now']['windSpeed']),
                'weatherWindDirection': Template('${direction}').substitute(
                    direction=forecast['now']['windFromDirection']
                ),
                'weatherPrecipitation': Template('${precipitation} mm').substitute(
                    precipitation=forecast['next6Hours']['precipitationAmount']
                ),
            }
        )

        logger.info('Writing images')
        self.note.write('./img-black.bmp', './img-colour.bmp')

        if self.updateDisplay:
            logger.info('Updating display')
            displayArgs = ['python', '-m', 'display']
            if self.verbose:
                displayArgs.append('--verbose')
            if self.quiet:
                displayArgs.append('--quiet')
            displayArgs.extend(
                [
                    'render',
                    '-b',
                    './img-black.bmp',
                    '-c',
                    './img-colour.bmp',
                    '-r',
                    str(self.rotate),
                ]
            )

            try:
                subprocess.run(displayArgs, check=True)
            except subprocess.CalledProcessError as exc:
                logger.error('See above for details. %s', exc)
                sys.exit(1)

        logger.info('Run completed')
