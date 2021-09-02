"""Command Line Interface"""

import argparse
import logging
import os

from display.display import Display

logger = logging.getLogger(__name__)


def chechPathExists(path):
    """Throw if path doesn't exist"""
    if not os.path.exists(path):
        raise FileNotFoundError(path)


def checkValidRotation(rotationDegrees):
    """Throw if outside valid range: [0 - 359]"""
    if rotationDegrees < 0 or rotationDegrees > 359:
        raise ValueError('Rotation should be between 0 and 359')


def clear():
    """Clear display"""
    logger.debug('Clearing')
    display = Display()
    display.clear()


def render(args):
    """Render to display"""
    logger.debug('Rendering')

    blackImagePath = args.black_image[0]
    colourImagePath = args.colour_image[0]
    rotateDegrees = args.rotate[0]

    chechPathExists(blackImagePath)
    chechPathExists(colourImagePath)
    checkValidRotation(rotateDegrees)

    display = Display()
    display.render(blackImagePath, colourImagePath, rotateDegrees)


def cli():
    """CLI definition and execution"""
    programParser = argparse.ArgumentParser(description='Handles redering to an e-paper display over SPI on a Raspberry Pi',
                                            allow_abbrev=False)

    group = programParser.add_mutually_exclusive_group()
    group.add_argument('-v',
                       '--verbose',
                       action='store_true',
                       help='increase output verbosity')
    group.add_argument('-q',
                       '--quiet',
                       action='store_true',
                       help='decrease verbosity to absolute minimum')

    commandParsers = programParser.add_subparsers(dest='command', required=True, help='A command must be specified')

    commandParsers.add_parser('clear', help='Clear the screen')

    renderParser = commandParsers.add_parser('render', help='Render images to screen (clears before rendering)')
    renderParser.add_argument('-b',
                              '--black-image',
                              nargs=1,
                              required=True,
                              metavar='path',
                              help='Path to black part of image, required')
    renderParser.add_argument('-c',
                              '--colour-image',
                              nargs=1,
                              required=True,
                              metavar='path',
                              help='Path to color part of image, required')
    renderParser.add_argument('-r',
                              '--rotate',
                              default=0,
                              nargs=1,
                              type=int,
                              metavar='degrees',
                              help='Rotate image a number of degrees, defaults to 0')

    args = programParser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    elif args.quiet:
        logging.basicConfig(level=logging.WARNING)

    logger.debug('Parsed arguments %s', args)
    if args.command == 'clear':
        clear()
    elif args.command == 'render':
        render(args)
