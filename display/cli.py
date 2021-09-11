"""Command Line Interface"""

import argparse
import logging
import os

from common.cli_helpers import addVerboseAndQuiet, unfoldArgValueIfArrayOneFrom
from common.env_default import envDefault
from common.logger import setVerboseOrQuiet
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
    logger.info('Clearing')
    display = Display()
    display.clear()
    logger.info('Clearing completed')


def render(args):
    """Render to display"""
    logger.info('Rendering')

    blackImagePath = args.black_image
    colourImagePath = args.colour_image
    rotateDegrees = args.rotate

    chechPathExists(blackImagePath)
    chechPathExists(colourImagePath)
    checkValidRotation(rotateDegrees)

    display = Display()
    display.render(blackImagePath, colourImagePath, rotateDegrees)
    logger.info('Rendering completed')


def cli():
    """CLI definition and execution"""
    programParser = argparse.ArgumentParser(description='Handles redering to an e-paper display over SPI on a Raspberry Pi',
                                            allow_abbrev=False)

    verboseAndQuietGroup = programParser.add_mutually_exclusive_group()
    addVerboseAndQuiet(verboseAndQuietGroup)

    commandParsers = programParser.add_subparsers(dest='command', required=True, help='A command must be specified')

    commandParsers.add_parser('clear', help='Clear the screen')

    renderParser = commandParsers.add_parser('render', help='Render images to screen (clears before rendering)')
    renderParser.add_argument('-b',
                              '--black-image',
                              nargs=1,
                              action=envDefault('BLACK_IMAGE'),
                              required=True,
                              metavar='path',
                              help='Path to black part of image, required')
    renderParser.add_argument('-c',
                              '--colour-image',
                              nargs=1,
                              action=envDefault('COLOUR_IMAGE'),
                              required=True,
                              metavar='path',
                              help='Path to color part of image, required')
    renderParser.add_argument('-r',
                              '--rotate',
                              default=0,
                              action=envDefault('ROTATE'),
                              nargs=1,
                              type=int,
                              metavar='degrees',
                              help='Rotate image a number of degrees, defaults to 0')

    args = vars(programParser.parse_args())
    argsToUnfold = [
        'black_image',
        'colour_image',
        'rotate'
    ]
    args = unfoldArgValueIfArrayOneFrom(args, argsToUnfold)

    setVerboseOrQuiet(args.verbose, args.quiet)

    logger.debug('Parsed arguments %s', args)
    if args.command == 'clear':
        clear()
    elif args.command == 'render':
        render(args)
