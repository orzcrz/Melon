"""
Created by changrunze on 2024/5/12
Copyright © 2024 BaldStudio. All rights reserved.
"""

import pkgutil
import importlib


# 自动发现并导入当前包中的所有子模块
def import_submodules(package_name):
    package = importlib.import_module(package_name)
    for loader, module_name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_module_name = f"{package_name}.{module_name}"
        importlib.import_module(full_module_name)


# 调用函数进行子模块导入
import_submodules(__name__)

