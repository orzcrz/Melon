"""
Created by crzorz on 2024/08/20
Copyright © 2024 SHEIN. All rights reserved.
"""

import subprocess

from melon.foundation.logging import logger
from melon.foundation.global_def import git


class Workspace:
    def __init__(self):
        self._args_parser = None
        self._args = None

    @property
    def name(self):
        return 'workspace'

    @property
    def version(self):
        return '1.0.0'

    @property
    def help(self):
        return 'me workspace'

    @property
    def description(self):
        return '基于 git worktree 的快捷调用'

    @property
    def args_parser(self):
        return self._args_parser

    @args_parser.setter
    def args_parser(self, parser):
        self._args_parser = parser
        parser.add_argument('-a', '--add', nargs='?', const=True,
                            help='新建工作空间, 不指定名称则默认使用branch名称')
        parser.add_argument('-r', '--remove', nargs='?', const=True,
                            help='删除工作空间，不指定名称则默认使用branch名称')
        parser.add_argument('-b', '--branch',
                            help='指定分支名，不指定默认使用 add/remove 的参数')
        parser.add_argument('-t', '--track', nargs='?', const=True,
                            help='本地存在分支时，指定追踪远程同名分支')

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args):
        self._args = args
        if args.add:
            self.add_workspace(args)
        elif args.remove:
            self.remove_workspace(args)
        self.list_workspace()

    @staticmethod
    def _reset_name_and_branch(name):
        return name.replace('/', '_')

    @staticmethod
    def list_workspace():
        cmd = [
            git, 'worktree', 'list'
        ]
        logger.debug('Running: %r', cmd)
        logger.info('Here is Your Workspace 👇👇👇')
        subprocess.run(cmd)

    @staticmethod
    def add_workspace(args):
        branch = args.branch
        if isinstance(args.add, bool):
            if branch is None:
                logger.error('必须指定 workspace 关联的分支')
                return
            name = branch.strip().replace('/', '_')
        else:
            name = args.add.strip()
            if branch is None:
                branch = name.replace('/', '_')

        cmd = [
            git, 'worktree', 'add', '../%s' % name,
        ]
        if args.track:
            cmd.extend([
                '-B', branch, '--track', 'origin/%s' % branch
            ])
        else:
            cmd.extend([
                '-b', branch
            ])
        logger.debug('Running: %r', cmd)
        subprocess.check_output(cmd)

    @staticmethod
    def remove_workspace(args):
        branch = args.branch
        if isinstance(args.remove, bool):
            if branch is None:
                logger.error('必须指定 workspace 关联的分支')
                return
            name = branch.strip().replace('/', '_')
        else:
            name = args.remove.strip()
            if branch is None:
                branch = name.replace('/', '_')
        cmd = [
            git, 'worktree', 'remove', name, '--force'
        ]
        logger.debug('Running: %r', cmd)
        logger.warn('【 REMOVE 】%s,【 BRANCH 】%s', name, branch)
        subprocess.check_output(cmd)

        cmd = [
            git, 'branch', '-D', branch
        ]
        logger.debug('Running: %r', cmd)
        subprocess.check_output(cmd)
