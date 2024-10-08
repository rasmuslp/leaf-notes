"""Quote module"""

import logging
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


@dataclass
class Quote:
    """A quote"""

    author: str
    quote: str
    title: str


def isQuoteDefinitionValid(quoteDefinition):
    """Validate quote definition"""

    required = ['quote']
    requiredSatisfied = all(key in quoteDefinition for key in required)
    if not requiredSatisfied:
        logger.warning(
            '"quote" needs to be defined, but is missing for object: %s',
            quoteDefinition,
        )
        return False

    return True


def loadQuotes(path):
    """Returns Quote objects loaded from provided yaml path"""
    with Path(path).open(encoding='utf-8') as fileStream:
        try:
            quoteDefinitions = yaml.load(fileStream, Loader=yaml.SafeLoader)
        except yaml.YAMLError as exc:
            logger.error('Cannot parse %s %s', path, exc)
            sys.exit(1)

    quotes = [Quote(**data) for data in filter(isQuoteDefinitionValid, quoteDefinitions)]

    return quotes
