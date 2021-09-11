"""Note module"""
import copy

import epdlib
from PIL import Image

layoutBaseQuoteFullWeather = {
    'quoteText': {
        'type': 'TextBlock',
        'image': None,
        'max_lines': 5,
        'padding': 1,
        'width': 3 / 4,
        'height': 6 / 6,
        'abs_coordinates': (0, 0),
        'relative': False,
        'font': './notes/fonts/Roboto-LightItalic.ttf',
        'font_size': None,
        'mode': '1'
    },

    'weatherIcon': {
        'type': 'ImageBlock',
        'image': True,
        'padding': 1,
        'width': 1 / 4,
        'height': 3 / 6,
        'abs_coordinates': (None, 0),
        'hcenter': True,
        'vcenter': True,
        'relative': ['quoteText', 'weatherIcon'],
        'mode': '1'
    },

    'weatherTemperature': {
        'type': 'TextBlock',
        'image': None,
        'max_lines': 1,
        'padding': 1,
        'width': 1 / 4,
        'height': 1 / 6,
        'abs_coordinates': (None, None),
        'relative': ['quoteText', 'weatherIcon'],
        'font': './notes/fonts/Roboto-Regular.ttf',
        'font_size': None,
        'mode': '1'
    },

    # Also add direction somehow
    'weatherWindSpeed': {
        'type': 'TextBlock',
        'image': None,
        'max_lines': 1,
        'padding': 1,
        'width': 1 / 4,
        'height': 1 / 6,
        'abs_coordinates': (None, None),
        'relative': ['quoteText', 'weatherTemperature'],
        'font': './notes/fonts/Roboto-Regular.ttf',
        'font_size': None,
        'mode': '1'
    },

    'weatherPrecipitation': {
        'type': 'TextBlock',
        'image': None,
        'max_lines': 1,
        'padding': 1,
        'width': 1 / 4,
        'height': 1 / 6,
        'abs_coordinates': (None, None),
        'relative': ['quoteText', 'weatherWindSpeed'],
        'font': './notes/fonts/Roboto-Regular.ttf',
        'font_size': None,
        'mode': '1'
    },
}

blockQuoteTitle = {
    'type': 'TextBlock',
    'image': None,
    'max_lines': 1,
    'padding': 1,
    'width': 3 / 4,
    'height': 1 / 6,
    'abs_coordinates': (0, 0),
    'hcenter': False,
    'vcenter': True,
    'relative': False,
    'font': './notes/fonts/Roboto-Bold.ttf',
    'font_size': None,
    'mode': '1'
}

blockQuoteAuthor = {
    'type': 'TextBlock',
    'image': None,
    'max_lines': 1,
    'padding': 1,
    'width': 3 / 4,
    'height': 1 / 6,
    'abs_coordinates': (0, None),
    'relative': ['quoteAuthor', 'quoteText'],
    'font': './notes/fonts/Roboto-Regular.ttf',
    'font_size': None,
    'mode': '1'
}


class Note:
    """A Note to display that can be saved to disk"""
    def __init__(self):
        self.epdLayout = epdlib.Layout(resolution=(212, 104))

    def update(self, updates):
        """Set data"""
        theLayout = copy.deepcopy(layoutBaseQuoteFullWeather)
        if 'quoteTitle' in updates and updates['quoteTitle'] is not None:
            theLayout = {
                'quoteTitle': copy.deepcopy(blockQuoteTitle)
            }
            theLayout.update(copy.deepcopy(layoutBaseQuoteFullWeather))
            theLayout['quoteText']['abs_coordinates'] = (0, None)
            theLayout['quoteText']['relative'] = ['quoteText', 'quoteTitle']

        if 'quoteAuthor' in updates and updates['quoteAuthor'] is not None:
            theLayout['quoteAuthor'] = copy.deepcopy(blockQuoteAuthor)

        if ('quoteTitle' in updates and updates['quoteTitle'] is not None) != ('quoteAuthor' in updates and updates['quoteAuthor'] is not None):
            theLayout['quoteText']['height'] = 5 / 6
            theLayout['quoteText']['mac_lines'] = 6
        elif 'quoteTitle' in updates and updates['quoteTitle'] is not None and 'quoteAuthor' in updates and updates['quoteAuthor'] is not None:
            theLayout['quoteText']['height'] = 4 / 6

        self.epdLayout.layout = theLayout
        self.epdLayout.update_contents(updates)

    def write(self, blackImagePath, colourImagePath):
        """Write image to disk"""
        blackImage = Image.new('1', self.epdLayout.resolution, 1)
        colourImage = Image.new('1', self.epdLayout.resolution, 1)

        if 'quoteTitle' in self.epdLayout.blocks:
            blackImage.paste(self.epdLayout.blocks['quoteTitle'].image, self.epdLayout.blocks['quoteTitle'].abs_coordinates)

        blackImage.paste(self.epdLayout.blocks['quoteText'].image, self.epdLayout.blocks['quoteText'].abs_coordinates)

        if 'quoteAuthor' in self.epdLayout.blocks:
            colourImage.paste(self.epdLayout.blocks['quoteAuthor'].image, self.epdLayout.blocks['quoteAuthor'].abs_coordinates)

        blackImage.paste(self.epdLayout.blocks['weatherIcon'].image, self.epdLayout.blocks['weatherIcon'].abs_coordinates)
        blackImage.paste(self.epdLayout.blocks['weatherTemperature'].image, self.epdLayout.blocks['weatherTemperature'].abs_coordinates)
        blackImage.paste(self.epdLayout.blocks['weatherWindSpeed'].image, self.epdLayout.blocks['weatherWindSpeed'].abs_coordinates)
        blackImage.paste(self.epdLayout.blocks['weatherPrecipitation'].image, self.epdLayout.blocks['weatherPrecipitation'].abs_coordinates)

        blackImage.save(blackImagePath)
        colourImage.save(colourImagePath)
