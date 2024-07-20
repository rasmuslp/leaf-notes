"""Keyboard interrupt module"""

import signal
import sys


# pylint: disable=unused-argument
def handler(signum, frame):
    """Handle interrupt"""
    sys.exit(1)


def setupKeyboardInterruptHandler():
    """Register interrupt handler"""
    signal.signal(signal.SIGINT, handler)
