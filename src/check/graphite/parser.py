# encoding: utf-8
"""
check.graphite

Created by mpeeters
Licensed under the GPL license, see LICENCE.txt for more details.
Copyright by Affinitic sprl
"""

try:
    from argparse import ArgumentParser as Parser
    HAS_ARGPARSE = True
except ImportError:
    from optparse import OptionParser as Parser
    HAS_ARGPARSE = False


class ArgumentParser(Parser):

    def add_argument(self, *args, **kwargs):
        if HAS_ARGPARSE:
            return Parser.add_argument(self, *args, **kwargs)
        return Parser.add_option(self, *args, **kwargs)

    def parse_args(self):
        if HAS_ARGPARSE:
            return Parser.parse_args(self)
        return Parser.parse_args(self)[0]
