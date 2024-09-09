"""
Created by changrunze on 2024/5/12
Copyright © 2024 BaldStudio. All rights reserved.
"""

import errno
import os
import shutil


# 复制文件
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


# 生成软链
def symlink_force(src, dst, is_directory=False):
    src = os.path.abspath(src)
    dst = os.path.abspath(dst)
    try:
        os.symlink(src, dst, is_directory)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(dst)
            os.symlink(src, dst, is_directory)
        else:
            raise e
