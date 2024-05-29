#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio TOPTEK module. Place your Python package
description here (python/__init__.py).
'''
import os

# import pybind11 generated symbols into the toptek namespace
try:
    # this might fail if the module is python-only
    from .toptek_python import *
except ModuleNotFoundError:
    pass

# import any pure python here
from .toptek_control import toptek_control
from .digital_PTT import digital_PTT
#
