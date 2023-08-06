#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import standard
from pycif.utils.classes.obsvects import ObsVect

ObsVect.register_plugin('standard', 'std', standard)
