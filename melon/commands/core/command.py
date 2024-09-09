"""
Created by crzorz on 2024/09/09
Copyright © 2024 SHEIN. All rights reserved.
"""

import argparse

from . import __commands__


def command(cls):
    __commands__.append(cls)
    return cls


class Command:
    def __init__(self, cli_group):
        self.parser: argparse.ArgumentParser = cli_group.add_parser(self.name,
                                                                    help=self.help,
                                                                    description=self.description)
        self.args = None
        self.prepare_actions()

    @property
    def name(self):
        raise NotImplementedError

    @property
    def help(self):
        return f'me {self.name}'

    @property
    def description(self):
        return f'{self.name}'

    def prepare_actions(self):
        self.parser.add_argument('--verbose', action='store_true', default=False, help="详细输出")

    def run(self, args):
        self.args = args
