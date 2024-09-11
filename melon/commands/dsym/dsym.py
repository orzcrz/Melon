"""
Created by crzorz on 2024/09/09
Copyright © 2024 SHEIN. All rights reserved.
"""

import os
import subprocess

from melon.commands.core.command import command, Command
from melon.misc.logging import logger
from melon.misc.global_def import XCODE_SHARED_FRAMEWORKS

XCODE_CRASH_SYMBOLICATOR = os.path.join(
        XCODE_SHARED_FRAMEWORKS, 'CoreSymbolicationDT.framework/Versions/A/Resources/CrashSymbolicator.py')


@command
class Dsym(Command):

    @property
    def name(self):
        return 'dsym'

    @property
    def description(self):
        return '符号化 crash 文件'

    def prepare_actions(self):
        super().prepare_actions()
        self.parser.add_argument('file', type=str, help='指定 crash 文件路径')
        self.parser.add_argument('-d', '--dsym', type=str, required=True, help='指定产物符号 YOUR.app.dSYM 的文件路径')
        self.parser.add_argument('-o', '--output', type=str, help='输出文件路径，默认为指定 crash 文件的同目录下')
        self.parser.add_argument(
            '--dt', type=str, default=XCODE_CRASH_SYMBOLICATOR,
            help=f'指定 Xcode 的 CrashSymbolicator.py 脚本路径，默认为 {XCODE_CRASH_SYMBOLICATOR}')

    def run(self, args):
        super().run(args)
        self.symbolicate()

    def symbolicate(self, ):
        file = self.args.file
        if file.endswith('.crash'):
            logger.error('暂不支持符号化 .crash 文件，请重新指定为 .ips 文件')
            return
        if not file.endswith('.ips'):
            logger.error('请指定正确的文件路径')
            return

        logger.info(f'开始符号化文件：{file}')
        output_dir = self.args.output
        if not output_dir:
            output_dir = os.path.dirname(file)
            logger.debug(output_dir)
        filename = os.path.basename(file).split('.')[0] + '.crash.ips'
        output_file = os.path.join(output_dir, filename)
        cmd = [
            'python', self.args.dt,
            '-d', self.args.dsym,
            '-p', file,
            '-o', output_file
        ]
        subprocess.check_output(cmd)
        logger.info(f'符号化完成，结果保存在 {output_file}')
