from pprint import pprint
import random
import os

import yaml

from quote import Quote

stream = open('quotes.yml', 'r')
try:
    quoteDefinitions = yaml.load(stream, Loader=yaml.SafeLoader)
except yaml.YAMLError as exc:
    print('Cannot parse quotes.yml', exc)
    os._exit(1)

stream.close()


def isQuoteDefinitionValid(quoteDefinition):
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
