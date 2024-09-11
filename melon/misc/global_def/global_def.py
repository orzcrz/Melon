"""
Created by crzorz on 2024/07/15
Copyright © 2024 SHEIN. All rights reserved.
"""

import os
import subprocess
import shutil

GIT = shutil.which('git')
POD = shutil.which('pod')
GEM = shutil.which('gem')

"""
XCode Developer Path
"""

if shutil.which('xcode-select') is not None:
    XCODE_DEVELOPER_DIR = subprocess.check_output(['xcode-select', '-print-path']).decode().strip()
else:
    XCODE_DEVELOPER_DIR = '/Applications/Xcode.app/Contents/Developer'

XCODE_SHARED_FRAMEWORKS = os.path.join(XCODE_DEVELOPER_DIR, '../SharedFrameworks')
