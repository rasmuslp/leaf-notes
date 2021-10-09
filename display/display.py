"""Display module"""

from PIL import Image
from display.waveshare_epd import epd2in13b_V3


class Display:
    """Display - Facade for a Waveshare e-Paper / e-ink display"""
    def __init__(self):
        self.epd = epd2in13b_V3.EPD()

    def clear(self):
        """Clear display"""
        self.epd.init()
        self.epd.Clear()
        self.epd.sleep()

    def render(self, blackImagePath, colourImagePath, rotateDegrees):
        """Render to display"""
        self.epd.init()
        blackImage = Image.open(blackImagePath).rotate(rotateDegrees)
        colourImage = Image.open(colourImagePath).rotate(rotateDegrees)
        self.epd.display(self.epd.getbuffer(blackImage), self.epd.getbuffer(colourImage))
        self.epd.sleep()
