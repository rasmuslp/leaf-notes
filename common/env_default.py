"""Provides a utility to inject environment variables into argparse definitions.
Currently requires explicit naming of env vars to check for"""

import argparse
import os


# Courtesy of http://stackoverflow.com/a/10551190 with env-var retrieval fixed
class EnvDefault(argparse.Action):
    """An argparse action class that auto-sets missing default values from env
    vars. Defaults to requiring the argument."""

    def __init__(self, envvar, required=None, default=None, **kwargs):
        if envvar in os.environ:
            default = os.environ[envvar]
        if required and default:
            required = False
        super().__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def envDefault(envvar):
    """functional sugar for EnvDefault"""
    def wrapper(**kwargs):
        return EnvDefault(envvar, **kwargs)
    return wrapper
