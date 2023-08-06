# -*- coding: utf-8 -*-
"""Contains all recognized XXfluxXX formats.
Automatically loads all pre-defined models as sub-modules of pycif.models
"""

from os.path import dirname, basename, isdir
import glob

modules = glob.glob(dirname(__file__) + "/*")

__all__ = [basename(f) for f in modules
           if isdir(f) and not f.endswith('.py')]

import register
