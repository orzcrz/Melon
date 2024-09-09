"""
Created by crzorz on 2024/07/08
Copyright © 2024 SHEIN. All rights reserved.
"""

from melon.commands.core.command import command, Command
from melon.misc.logging import logger
from melon.misc.file import *


@command
class Config(Command):
    def __init__(self, cli_group):
        super().__init__(cli_group)
        self._root_dir = None
        self._xcode_dev_dir = None

    @property
    def name(self):
        return 'config'

    @property
    def description(self):
        return '个人配置项'

    def prepare_actions(self):
        super().prepare_actions()
        self.parser.add_argument('-a', '--all',
                                 const=True,
                                 nargs='?',
                                 help='更新所有类型的配置')
        self.parser.add_argument('--xctemplate',
                                 const=True,
                                 nargs='?',
                                 help='更新 Xcode 模板')
        self.parser.add_argument('--code-snippet',
                                 const=True,
                                 nargs='?',
                                 help='更新 Xcode 代码片段')

    def run(self, args):
        super().run(args)
        self._root_dir = os.environ['MELON_ROOT']
        self._xcode_dev_dir = os.path.expanduser('~/Library/Developer/Xcode')
        if args.all:
            logger.info('更新所有配置')
            self._update_xctemplate()
            self._update_code_snippet()
            return
        if args.xctemplate:
            logger.info('更新 Xcode 模板')
            self._update_xctemplate()
        if args.code_snippet:
            logger.info('更新 Xcode 代码片段')
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
