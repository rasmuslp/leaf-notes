"""Note module"""

import epdlib
from PIL import Image

layout1 = {
    'quoteTitle': {
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
    },
    'quoteText': {
        'type': 'TextBlock',
        'image': None,
        'max_lines': 5,
        'padding': 1,
        'width': 3 / 4,
        'height': 4 / 6,
        'abs_coordinates': (0, None),
        'relative': ['quoteText', 'quoteTitle'],
        'font': './notes/fonts/Roboto-LightItalic.ttf',
        'font_size': None,
        'mode': '1'
    },

    'quoteAuthor': {
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
        'relative': ['quoteTitle', 'weatherIcon'],
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
        'relative': ['quoteTitle', 'weatherIcon'],
        'font': './notes/fonts/Roboto-Regular.ttf',
        'font_size': None,
        'mode': '1'
    },

    'weatherWindSpeed': {
        'type': 'TextBlock',
        'image': None,
        'max_lines': 1,
        'padding': 1,
        'width': 1 / 4,
        'height': 1 / 6,
        'abs_coordinates': (None, None),
        'relative': ['quoteTitle', 'weatherTemperature'],
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
        'relative': ['quoteTitle', 'weatherWindSpeed'],
        'font': './notes/fonts/Roboto-Regular.ttf',
        'font_size': None,
        'mode': '1'
    },
}


class Note:
    """A Note to display that can be saved to disk"""
    def __init__(self):
        self.epdLayout = epdlib.Layout(resolution=(212, 104))
        self.epdLayout.layout = layout1

    def update(self, updates):
        """Set data"""
        self.epdLayout.update_contents(updates)

    def write(self, blackImagePath, colourImagePath):
        """Write image to disk"""
        blackImage = Image.new('L', self.epdLayout.resolution, 255)
        colourImage = Image.new('L', self.epdLayout.resolution, 255)

        blackImage.paste(self.epdLayout.blocks['quoteTitle'].image, self.epdLayout.blocks['quoteTitle'].abs_coordinates)
        blackImage.paste(self.epdLayout.blocks['quoteText'].image, self.epdLayout.blocks['quoteText'].abs_coordinates)
        colourImage.paste(self.epdLayout.blocks['quoteAuthor'].image, self.epdLayout.blocks['quoteAuthor'].abs_coordinates)
        blackImage.paste(self.epdLayout.blocks['weatherIcon'].image, self.epdLayout.blocks['weatherIcon'].abs_coordinates)
        blackImage.paste(self.epdLayout.blocks['weatherTemperature'].image, self.epdLayout.blocks['weatherTemperature'].abs_coordinates)
        blackImage.paste(self.epdLayout.blocks['weatherWindSpeed'].image, self.epdLayout.blocks['weatherWindSpeed'].abs_coordinates)
        blackImage.paste(self.epdLayout.blocks['weatherPrecipitation'].image, self.epdLayout.blocks['weatherPrecipitation'].abs_coordinates)

        blackImage.save(blackImagePath)
        colourImage.save(colourImagePath)
