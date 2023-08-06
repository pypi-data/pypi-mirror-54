#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import standard
from pycif.utils.classes.obsoperators import ObsOperator

ObsOperator.register_plugin('standard', 'std', standard)
