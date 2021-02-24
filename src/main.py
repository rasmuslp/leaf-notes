from pprint import pprint
import random
import os

import yaml

from Quote import Quote

stream = open('quotes.yml', 'r')
try:
    quoteDefinitions = yaml.load(stream, Loader=yaml.SafeLoader)
except yaml.YAMLError as exc:
    print('Cannot parse quotes.yml', exc)
    os._exit(1)

stream.close()


def createQuote(data):
    required = ['quote']
    requiredSatisfied = all(key in data.keys() for key in required)
    if not requiredSatisfied:
        print('"quote" needs to be defined, but is missing for object:')
        pprint(data)
        print()
        return

    return Quote(**data)


quotes = list(filter(None, map(createQuote, quoteDefinitions)))
randomQuote = random.choice(quotes)
print(randomQuote.quote)
print('                - ' + randomQuote.author)
