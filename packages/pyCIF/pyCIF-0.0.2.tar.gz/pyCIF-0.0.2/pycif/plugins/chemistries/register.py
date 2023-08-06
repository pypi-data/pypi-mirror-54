#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import chimere
from pycif.utils.classes.chemistries import Chemistry

Chemistry.register_plugin('CHIMERE', 'gasJtab', chimere)

del chimere
