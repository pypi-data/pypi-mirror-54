#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import gausscost
from . import dummy
from pycif.utils.classes.simulators import Simulator

Simulator.register_plugin('gausscost', 'std', gausscost)
Simulator.register_plugin('dummy_txt', 'std', dummy)
