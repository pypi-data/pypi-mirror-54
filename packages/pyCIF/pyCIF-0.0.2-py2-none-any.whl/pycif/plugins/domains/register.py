#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import lmdz
from . import chimere
from . import dummy
from pycif.utils.classes.domains import Domain

Domain.register_plugin('LMDZ', 'std', lmdz)
Domain.register_plugin('CHIMERE', 'std', chimere)
Domain.register_plugin('dummy', 'std', dummy)

del lmdz
del chimere
