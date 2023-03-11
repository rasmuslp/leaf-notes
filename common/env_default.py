"""Provides a utility to inject environment variables into argparse definitions.
Currently requires explicit naming of env vars to check for"""

import argparse
import os


# Courtesy of http://stackoverflow.com/a/10551190 with env-var retrieval fixed and support for using with store_true
class EnvDefault(argparse.Action):
    """An argparse action class that auto-sets missing default values from env
    vars. Defaults to requiring the argument."""

    # pylint: disable=too-many-arguments
    def __init__(self, envvar, const=None, default=None, nargs=None, required=None, subAction=None, **kwargs):
        self.subAction = None
        if subAction:
            self.subAction = subAction
            if subAction == 'store_true':
                const = True
                default = False
                nargs = 0
            else:
                raise ValueError(f'subAction not recognized: {subAction}')

        if envvar in os.environ:
            default = os.environ[envvar]

        if required and default:
            required = False

        super().__init__(const=const, default=default, nargs=nargs, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if self.subAction:
            setattr(namespace, self.dest, self.const)
        else:
            setattr(namespace, self.dest, values)


def envDefault(envvar):
    """functional sugar for EnvDefault"""
    def wrapper(**kwargs):
        return EnvDefault(envvar, **kwargs)
    return wrapper
