"""CLI helpers"""
import copy
from types import SimpleNamespace

from common.env_default import envDefault


def addVerboseAndQuiet(mutualExclusiveGroup):
    """Add 'verbose' and 'quiet' options to group"""
    mutualExclusiveGroup.add_argument('-v',
                                      '--verbose',
                                      action=envDefault('VERBOSE'),
                                      default=False,
                                      type=bool,
                                      help='increase output verbosity')
    mutualExclusiveGroup.add_argument('-q',
                                      '--quiet',
                                      action=envDefault('QUIET'),
                                      default=False,
                                      type=bool,
                                      help='decrease verbosity to absolute minimum')


def unfoldArgValueIfArrayOneFrom(allArgs, toUnfold):
    """Processes a dict of args. Unfolds values - of keys in provided list - that are arrays with a single item"""
    args = copy.deepcopy(allArgs)

    for arg in toUnfold:
        argExistsAndIsArrayOfLength1 = arg in args and isinstance(args[arg], list) and len(args[arg]) == 1
        if argExistsAndIsArrayOfLength1:
            args[arg] = args[arg][0]

    namespaced = SimpleNamespace(**args)

    return namespaced
