"""
Created by changrunze on 2024/5/11
Copyright © 2024 BaldStudio. All rights reserved.
"""

import argparse
import sys
import time

from melon import __version__
from melon.subcommands import __subcommands__
from melon.foundation.logging import *

'''
命令行解释器
'''
parser = argparse.ArgumentParser(prog='me',
                                 description='命令行工具箱',
                                 epilog='工具箱版本 %s' % __version__)

parser.add_argument('--verbose',
                    action='store_true',
                    default=False,
                    help='详细输出')

parser.add_argument('--version',
                    action='version',
                    help='工具箱版本',
                    version=__version__)

'''
子命令解释器
'''
subcommand_parser = parser.add_subparsers(title='目前支持的功能', dest='command')
subcommands_by_name = {}

for command_class in __subcommands__:
    cmd = command_class()
    cmd.args_parser = subcommand_parser.add_parser(cmd.name,
                                                   help=cmd.help,
                                                   description=cmd.description)
    cmd.args_parser.add_argument('--verbose',
                                 action='store_true',
                                 default=False,
                                 help='详细输出')
    subcommands_by_name[cmd.name] = cmd


def main():
    args = parser.parse_args()
    # 设置日志输出级别
    if args.verbose:
        logger.set_level(LogLevel.DEBUG)
    else:
        logger.set_level(LogLevel.INFO)

    logger.debug('当前命令行参数: %s' % args)

    subcommand = subcommands_by_name.get(args.command)
    if subcommand is None:
        parser.print_help()
    else:
        begin_time_ms = time.time() * 1000
        subcommand.args = args
        cost = time.time() * 1000 - begin_time_ms
        logger.debug('TOTAL COST: {:.4f} ms'.format(cost))


if __name__ == '__main__':
    main()
