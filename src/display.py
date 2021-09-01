"""Entry point of the 'display' application"""

import argparse


def clear():
    """Clear display"""
    print('Clearing')


def render(args):
    """Render to display"""
    print('Rendering', args)


def main():
    """display main function"""
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
                              '--image-black',
                              nargs=1,
                              required=True,
                              metavar='path',
                              help='Path to black part of image, required')
    renderParser.add_argument('-c',
                              '--image-colour',
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
    if args.command == 'clear':
        clear()
    elif args.command == 'render':
        render(args)


if __name__ == '__main__':
    main()
