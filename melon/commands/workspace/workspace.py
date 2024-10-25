"""
Created by crzorz on 2024/08/20
Copyright © 2024 SHEIN. All rights reserved.
"""

import subprocess

from melon.commands.core.command import command, Command
from melon.misc.logging import logger
from melon.misc.global_def import GIT


@command
class Workspace(Command):
    def __init__(self, cli_group):
        super().__init__(cli_group)

    @property
    def name(self):
        return 'workspace'

    @property
    def description(self):
        return '基于 git worktree 的快捷调用'

    def prepare_actions(self):
        super().prepare_actions()
        self.parser.add_argument('-a', '--add', nargs='?', const=True,
                            help='新建工作空间, 不指定名称则默认使用branch名称')
        self.parser.add_argument('-r', '--remove', nargs='?', const=True,
                            help='删除工作空间，不指定名称则默认使用branch名称')
        self.parser.add_argument('-b', '--branch',
                            help='指定分支名，不指定默认使用 add/remove 的参数')
        self.parser.add_argument('-t', '--track', nargs='?', const=True,
                            help='本地存在分支时，指定追踪远程同名分支')
        self.parser.add_argument('-l', '--list', nargs='?', const=True,
                            help='列出所有工作空间')

    def run(self, args):
        super().run(args)
        if args.add:
            self._add_workspace()
        elif args.remove:
            self._remove_workspace()
        else:
            self._list_workspace()

    @staticmethod
    def _list_workspace():
        cmd = [
            GIT, 'worktree', 'list'
        ]
        logger.debug('Running: %r', cmd)
        logger.info('Here is Your Workspace 👇👇👇')
        subprocess.run(cmd)

    def _add_workspace(self):
        branch = self.args.branch
        if branch is None:
            logger.error('必须指定 workspace 关联的分支')
            return
        if isinstance(self.args.add, bool):
            name = branch.replace('/', '_')
        else:
            name = self.args.add.strip()

        cmd = [
            GIT, 'worktree', 'add', '../%s' % name,
        ]
        if self.args.track:
            cmd.extend([
                '-B', branch, '--track', 'origin/%s' % branch
            ])
        else:
            cmd.extend([
                '-b', branch
            ])
        logger.debug('Running: %r', cmd)
        subprocess.check_output(cmd)

    def _remove_workspace(self):
        branch = self.args.branch
        if branch is None:
            logger.error('必须指定 workspace 关联的分支')
            return
        if isinstance(self.args.remove, bool):
            name = branch.replace('/', '_')
        else:
            name = self.args.remove.strip()

        cmd = [
            GIT, 'worktree', 'remove', name, '--force'
        ]
        logger.debug('Running: %r', cmd)
        logger.warn('【 REMOVE 】%s,【 BRANCH 】%s', name, branch)
        subprocess.check_output(cmd)

        cmd = [
            GIT, 'branch', '-D', branch
        ]
        logger.debug('Running: %r', cmd)
        subprocess.check_output(cmd)
