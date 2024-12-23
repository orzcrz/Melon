"""
Created by changrunze on 2024/5/12
Copyright © 2024 BaldStudio. All rights reserved.
"""

import os
import subprocess
import tempfile
import json

from melon.misc.file import symlink_force
from melon.misc.logging import logger
from melon.misc.global_def import POD, GEM
from .git import Git

POD_SPEC_REPO_NAME = os.environ.get('POD_SPEC_REPO_NAME', 'baldstudio')
POD_SPEC_REPO_URL = os.environ.get('POD_SPEC_REPO_URL', 'git@github.com:BaldStudio/baldstudio-specs.git')
POD_SPEC_REPO_ROOT_DIR = os.environ.get('POD_SPEC_REPO_ROOT_DIR', os.path.join(os.path.expanduser('~'), '.cocoapods/repos'))

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
POD_PATCH_DIR = os.path.join(CURRENT_DIR, 'cocoapods_patches')
POD_PLUGIN_DIR = os.path.join(CURRENT_DIR, 'cocoapods_plugins')

class Pod:
    @staticmethod
    def find_podspec_file(target):
        podspec_file = target
        if not podspec_file:
            logger.debug('未指定 podspec_file，将自动查找当前目录下首个匹配项')
            for f in os.listdir(os.getcwd()):
                if f.endswith('.podspec'):
                    podspec_file = f
                    break
        if not podspec_file:
            logger.error('未找到 podspec 文件')
            return
        logger.debug('找到 podspec 文件：%s', podspec_file)
        return podspec_file

    @staticmethod
    def generate_podspec_json(target):
        podspec_file = Pod.find_podspec_file(target)
        if not podspec_file:
            return
        temp_dir = tempfile.mkdtemp()
        podspec_json = os.path.join(temp_dir, podspec_file + '.json')
        with open(podspec_json, 'w') as f:
            cmd = [
                POD, 'ipc', 'spec', podspec_file,
            ]
            logger.debug('Running: %r', ' '.join(cmd))
            subprocess.Popen(cmd, stdout=f).wait()
        logger.debug('生成 podspec json 文件：%s', podspec_json)
        return podspec_json

    @staticmethod
    def update_podspec_json(podspec_json, version):
        logger.debug('修改版本号为 %s', version)
        with open(podspec_json, 'r') as f:
            json_data = json.load(f)
            json_data['version'] = version
            json_data['source']['tag'] = version
            json_data['source']['commit'] = Git.head
            logger.debug(json_data)
        with open(podspec_json, 'w') as f:
            if json_data:
                f.write(json.dumps(json_data, indent=2))

    @staticmethod
    def push_spec_to_remote(podspec_file, source):
        source = source or POD_SPEC_REPO_NAME
        logger.debug(f'发布 podspec 到 {source}')
        repo_name = Pod.find_pod_repo_dir_name(source)
        cmd = [
            POD, 'repo', 'push', repo_name, podspec_file,
            '--allow-warnings',
            '--force',
        ]
        logger.debug('Running: %r', ' '.join(cmd))
        subprocess.check_output(cmd)

    @staticmethod
    def install_plugins():
        cmd = [
            GEM, 'install',
        ]
        plugin_dir = POD_PLUGIN_DIR
        for root, _, files in os.walk(plugin_dir):
            for f in files:
                if f.endswith('.gem'):
                    src_file = os.path.join(root, f)
                    src_file = os.path.abspath(src_file)
                    logger.debug('🩹 找到插件文件 %s' % src_file)
                    logger.info('🩹 安装插件 %s' % src_file)
                    cmd.append(src_file)
        logger.debug('Running: %r', ' '.join(cmd))
        subprocess.check_output(cmd)

    # 给 cocoapods 打补丁
    @staticmethod
    def install_patches():
        cocoapods_dir = Pod.find_cocoapods_dir()
        if not cocoapods_dir:
            logger.error('cocoapods path is not found')
            return
        patch_dir = POD_PATCH_DIR
        for root, _, files in os.walk(patch_dir):
            for f in files:
                if f.endswith('.rb'):
                    src_file = os.path.join(root, f)
                    logger.debug('🩹 找到补丁文件 %s' % src_file)
                    # 找到对应文件替换
                    dst_file = Pod.find_cocoapods_file(cocoapods_dir, f, os.path.basename(root))
                    if not dst_file:
                        logger.warn('未找到补丁对应的源文件')
                        continue
                    symlink_force(src_file, os.path.abspath(dst_file))
                    logger.info('🩹 替换文件 %s' % dst_file)

    # 查找 cocoapods 源码路径
    @staticmethod
    def find_cocoapods_dir() -> str:
        cmd = [
            GEM, 'which', 'cocoapods',
        ]
        logger.debug('Running: %r', ' '.join(cmd))
        cocoapods_dir = subprocess.check_output(cmd).decode()
        cocoapods_dir = os.path.abspath(os.path.join(cocoapods_dir, '..', 'cocoapods'))
        logger.debug('🩹 find cocoapods dir %s' % cocoapods_dir)
        return cocoapods_dir

    @staticmethod
    def find_pod_repo_dir_name(source):
        logger.debug(f'寻找私有仓库 {source} 目录')
        repos_dir = POD_SPEC_REPO_ROOT_DIR
        for d in os.listdir(repos_dir):
            if d == source:
                os.chdir(os.path.join(repos_dir, d))
                current = Git.remote_url
                logger.debug(f'当前私有仓库名称为 {d}，地址为 {current}')
                return d
        logger.error('找不到 %s 仓库', POD_SPEC_REPO_NAME)
    
    # 查找补丁对应的 cocoapods 源文件
    @staticmethod
    def find_cocoapods_file(cocoapods_dir, target_file, basename) -> str:
        for root, _, files in os.walk(cocoapods_dir):
            for f in files:
                # 为了避免找到不同路径下的同名文件，增加上级目录的比较
                if f == target_file and os.path.basename(root) == basename:
                    path = os.path.join(root, f)
                    logger.debug('🩹 find cocoapods file %s' % path)
                    return str(path)
