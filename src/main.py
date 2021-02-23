import random

from Quote import Quote

quotes = []

qoutes.append(Quote('Yogi Bhajan', 'The greatest education man has to learn is the science of self.'))
qoutes.append(Quote('Yogi Bhajan', 'When the prayer becomes the vibration of the mind and self, then we can create a miracle.', 'PRAY'))
qoutes.append(Quote('Yogi Bhajan', 'There are three values: Feel good, be good and do good.'))
qoutes.append(Quote('Yogi Bhajan', 'Consult your spirit, your soul on everything.', 'LISTEN'))
qoutes.append(Quote('Yogi Bhajan', 'If you are happy, happiness will come to you because happiness wants to go where happiness is.', 'BE LIGHT'))

randomQuote = random.choise(quotes)

print(randomQuote)