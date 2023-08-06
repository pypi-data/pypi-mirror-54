#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycif.utils.classes.controlvects import ControlVect
from . import standard

ControlVect.register_plugin('standard', 'std', standard)
