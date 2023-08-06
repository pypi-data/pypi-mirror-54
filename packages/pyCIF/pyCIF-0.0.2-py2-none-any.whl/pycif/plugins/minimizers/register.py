#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycif.utils.classes.minimizers import Minimizer
from . import m1qn3
from . import congrad

Minimizer.register_plugin('M1QN3', 'std', m1qn3)
Minimizer.register_plugin('congrad', 'std', congrad)
