"""
Created by changrunze on 2024/5/11
Copyright © 2024 BaldStudio. All rights reserved.
"""

import argparse
import time

from melon import __version__
from melon.commands.core import __commands__
from melon.misc.logging import *


def main():
    begin_time_ms = time.time() * 1000

    args = cli.parse_args()

    if args.verbose:
        logger.set_level(LogLevel.DEBUG)
    else:
        logger.set_level(LogLevel.INFO)

    logger.debug('当前命令行参数: %s' % args)

    if not args.command:
        cli.print_help()
        return

    command = commands_by_name.get(args.command)
    if command is None:
        logger.error(f'未知命令: {args.command}')
    else:
        command.run(args)

    cost = time.time() * 1000 - begin_time_ms
    logger.debug('TOTAL COST: {:.4f} ms'.format(cost))


def make_cli():
    _cli = argparse.ArgumentParser(prog='me',
                                   description='开发百宝箱',
                                   epilog='版本 %s' % __version__)
    _cli.add_argument('--verbose',
                      action='store_true',
                      default=False,
                      help='详细输出')
    _cli.add_argument('--version',
                      action='version',
                      help='当前版本',
                      version=__version__)
    return _cli


def make_cli_group():
    _cli_group = cli.add_subparsers(title="目前支持的功能", dest="command")
    return _cli_group


def prepare_commands():
    _commands_by_name = {}
    for cmd_class in __commands__:
        cmd = cmd_class(cli_group)
        _commands_by_name[cmd.name] = cmd
    return _commands_by_name


if __name__ == '__main__':
    cli = make_cli()
    cli_group = make_cli_group()
    commands_by_name = prepare_commands()
    main()
