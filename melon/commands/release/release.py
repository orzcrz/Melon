"""
Created by changrunze on 2024/5/12
Copyright © 2024 BaldStudio. All rights reserved.
"""

import os
import time

from melon.misc.loader import Loader
from melon.misc.logging import logger

from .pod import Pod
from .git import Git

from melon.commands.core.command import command, Command


@command
class Release(Command):
    def __init__(self, cli_group):
        super().__init__(cli_group)
        self._loading = None

    @property
    def name(self):
        return 'release'

    @property
    def description(self):
        return '发布私有 Pod 的工具，支持 SNAPSHOT 版本'

    def prepare_actions(self):
        super().prepare_actions()
        self.parser.add_argument('--pod-patch',
                                 const=True,
                                 nargs='?',
                                 help='增加 pod 补丁，按照当前 pod 版本的路径添加')
        self.parser.add_argument('--pod-plugin',
                                 const=True,
                                 nargs='?',
                                 help='增加 pod 插件，按照当前 pod 版本的路径添加')
        self.parser.add_argument('--podspec',
                                 type=str,
                                 help='指定 podspec 发布')
        self.parser.add_argument('version',
                                 type=str,
                                 help='参数为版本号，默认发布 SNAPSHOT 版本，发布正式版需要带上--stable')
        self.parser.add_argument('--stable',
                                 const=True,
                                 nargs='?',
                                 help='发布正式版')
        self.parser.add_argument('-s', '--source',
                                 type=str,
                                 help='指定源，名字就可以，可以通过 pod repo list 查看当前源信息')

    def run(self, args):
        super().run(args)
        Git.verbose = args.verbose
        if args.pod_patch:
            Pod.install_patches()
            return True
        if args.pod_plugin:
            Pod.install_plugins()
            return True
        env = '正式版本' if args.stable else '开发版本'
        logger.info('📌 确认发布版本 [ %s ]' % env)
        time.sleep(1)
        if not self._preflight(args):
            return
        self._releasing(args)

    def _releasing(self, args):
        version = args.version
        if args.stable:
            if Git.has_tag(version):
                logger.error('版本号 %s 已存在', version)
                return False
        else:
            version += '-SNAPSHOT'
        logger.info('🍘 准备发布版本 %s' % version)
        self._start_loading()

        Git.tagging_forced(version)
        Git.push_tag_to_remote_forced(version)

        podspec_json = Pod.generate_podspec_json(args.podspec)
        if not podspec_json:
            return False
        Pod.update_podspec_json(podspec_json, version)
        Pod.push_spec_to_remote(podspec_json, args.source)

        self._end_loading()
        self._postflight()
        return True

    @staticmethod
    def _preflight(args):
        if not Git.is_valid_repo:
            logger.error('not a git repository (or any of the parent directories): .git')
            return False
        if not args.podspec and not any(name.endswith('.podspec') for name in os.listdir(os.getcwd())):
            logger.error('找不到 podspec 文件')
            return False
        if Git.has_any_changed:
            logger.error('local git repository must be clean')
            return False
        Git.fetch_forced()
        return True

    @staticmethod
    def _postflight():
        logger.info('🎉 发布成功')

    def _start_loading(self):
        self._loading = Loader('☕️ 正在发布...', '', 0.05).start()

    def _end_loading(self):
        self._loading.stop()
