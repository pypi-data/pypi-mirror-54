#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lmdz
import chimere
import dummy
from pycif.utils.classes.models import Model

Model.register_plugin('LMDZ', 'std', lmdz)
Model.register_plugin('CHIMERE', 'std', chimere)
Model.register_plugin('dummy', 'std', dummy)
