#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycif.utils.classes.measurements import Measurement

import standard
import random

Measurement.register_plugin('standard', 'std', standard)
Measurement.register_plugin('random', 'std', random)
