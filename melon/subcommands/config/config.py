"""
Created by crzorz on 2024/07/08
Copyright © 2024 SHEIN. All rights reserved.
"""

import os
from melon.foundation.logging import logger
from melon.foundation.file import *


class Config:
    def __init__(self):
        self._args_parser = None
        self._args = None
        self._root_dir = None
        self._xcode_dev_dir = None

    @property
    def name(self):
        return 'config'

    @property
    def help(self):
        return 'me config'

    @property
    def description(self):
        return '个人配置项'

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        self._args = args
        self._root_dir = os.environ['MELON_ROOT']
        self._xcode_dev_dir = os.path.expanduser('~/Library/Developer/Xcode')
        self._running(args)

    @property
    def args_parser(self):
        return self._args_parser

    @args_parser.setter
    def args_parser(self, parser):
        self._args_parser = parser
        parser.add_argument('--xctemplate',
                            const=True,
                            nargs='?',
                            help='更新 Xcode 模板')
        parser.add_argument('--code-snippet',
                            const=True,
                            nargs='?',
                            help='更新 Xcode 代码片段')

    def _running(self, args):
        if args.xctemplate:
            self._update_xctemplate()
        if args.code_snippet:
            self._update_code_snippet()

    def _update_xctemplate(self):
        xcode_template_path = os.path.join(self._xcode_dev_dir, 'Templates')
        logger.debug(f'xcode_template_path: {xcode_template_path}')
        xctemplates_dir = os.path.join(self._root_dir, 'profiles/xctemplates')
        logger.debug(f'xctemplates_dir: {xctemplates_dir}')

        # cc file template
        cc_template_name = 'CC File.xctemplate'
        cc_template_path = os.path.join(xcode_template_path, "File Templates/MultiPlatform/Source")
        os.makedirs(cc_template_path, exist_ok=True)
        logger.debug(f'cc_template_path: {cc_template_path}')
        source_dir = os.path.join(xctemplates_dir, cc_template_name)
        target_dir = os.path.join(cc_template_path, cc_template_name)
        symlink_force(source_dir, target_dir, is_directory=True)
        logger.info(f'更新 {cc_template_name}')

    def _update_code_snippet(self):
        xcode_user_data_path = os.path.join(self._xcode_dev_dir, 'UserData')
        logger.debug(f'xcode_user_data: {xcode_user_data_path}')
        source_dir = os.path.join(self._root_dir, 'profiles/CodeSnippets')
        target_dir = os.path.join(xcode_user_data_path, "CodeSnippets")
        symlink_force(source_dir, target_dir, is_directory=True)
        logger.info(f'更新 CodeSnippets')



