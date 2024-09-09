"""
Created by changrunze on 2024/5/12
Copyright © 2024 BaldStudio. All rights reserved.
"""

import subprocess

from melon.misc.global_def import git
from melon.misc.logging import logger
from melon.misc.annotations import classproperty


class Git:
    verbose = False

    def __init__(self):
        pass

    @classproperty
    def is_valid_repo(self):
        cmd = [
            git, 'rev-parse', '--is-inside-work-tree'
        ]
        logger.debug('Running: %r', cmd)
        if Git.verbose:
            return subprocess.check_output(cmd).decode()
        process = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
        result = str(process.communicate()[0].strip())
        return len(result) > 0

    @classproperty
    def head(cls):
        cmd = [
            git, 'rev-parse', '--short', 'HEAD'
        ]
        logger.debug('Running: %r', cmd)
        process = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
        return str(process.communicate()[0].strip())

    # 检查 git 是否有改动
    @classproperty
    def has_any_changed(self):
        cmd = [
            git, 'status', '--porcelain',
        ]
        logger.debug('Running: %r', cmd)
        result = subprocess.check_output(cmd)
        return bool(result.decode())

    @classproperty
    def remote_url(self):
        cmd = [
            git, 'ls-remote', '--get-url', 'origin'
        ]
        logger.debug('Running: %r', cmd)
        return subprocess.check_output(cmd).decode().strip()

    @staticmethod
    def fetch_forced():
        cmd = [
            git, 'fetch', '-f', '--tag'
        ]
        logger.debug('Running: %r', cmd)
        subprocess.check_output(cmd)

    @staticmethod
    def has_tag(tag: str) -> bool:
        cmd = [
            git, 'tag', '-l', tag
        ]
        logger.debug('Running: %r', cmd)
        if Git.verbose:
            return tag == subprocess.check_output(cmd).decode().strip()
        process = subprocess.Popen(cmd,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
        return tag == process.communicate()[0].strip()

    @staticmethod
    def tagging(version):
        cmd = [
            git, 'tag', '-a', version, '-m', 'v%s' % version
        ]
        logger.debug('Running: %r', cmd)
        subprocess.check_output(cmd)

    @staticmethod
    def tagging_forced(version):
        cmd = [
            git, 'tag', '-af', version, '-m', 'v%s' % version
        ]
        logger.debug('Running: %r', cmd)
        subprocess.check_output(cmd)

    @staticmethod
    def push_tag_to_remote(version):
        cmd = [
            git, 'push', 'origin', version
        ]
        logger.debug('Running: %r', cmd)
        if Git.verbose:
            subprocess.check_output(cmd)
        else:
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @staticmethod
    def push_tag_to_remote_forced(version):
        cmd = [
            git, 'push', '-f', 'origin', version
        ]
        logger.debug('Running: %r', cmd)
        if Git.verbose:
            subprocess.check_output(cmd)
        else:
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
