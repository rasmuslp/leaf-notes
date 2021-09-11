"""Entry point of the 'notes' application"""

from common.keyboard_interrupt import setupKeyboardInterruptHandler
from notes.cli import cli


if __name__ == '__main__':
    setupKeyboardInterruptHandler()
    cli()
