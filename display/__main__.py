"""Entry point of the 'display' application"""

from common.keyboard_interrupt import setupKeyboardInterruptHandler
from display.cli import cli

if __name__ == '__main__':
    setupKeyboardInterruptHandler()
    cli()
