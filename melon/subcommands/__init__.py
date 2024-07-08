"""
Created by changrunze on 2024/5/12
Copyright © 2024 BaldStudio. All rights reserved.
"""

from .release import Release
from .config import Config

__subcommands__ = [
    Release,
    Config,
]