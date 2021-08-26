"""Entry point of the application"""

from pprint import pprint
import random
import sys

import yaml

from quote import Quote

with open('quotes.yml', 'r', encoding='utf-8') as fileStream:
    try:
        quoteDefinitions = yaml.load(fileStream, Loader=yaml.SafeLoader)
    except yaml.YAMLError as exc:
        print('Cannot parse quotes.yml', exc)
        sys.exit(1)


def isQuoteDefinitionValid(quoteDefinition):
    """Validate qoute definition"""

    required = ['quote']
    requiredSatisfied = all(key in quoteDefinition.keys() for key in required)
    if not requiredSatisfied:
        print('"quote" needs to be defined, but is missing for object:')
        pprint(quoteDefinition)
        print()
        return False

    return True


quotes = list(map(lambda data: Quote(**data), filter(isQuoteDefinitionValid, quoteDefinitions)))
randomQuote = random.choice(quotes)
print(randomQuote.quote)
print('                - ' + randomQuote.author)
