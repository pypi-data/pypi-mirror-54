#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chimere_icbc
import lmdz_ic
from pycif.utils.classes.fields import Fields

Fields.register_plugin('CHIMERE', 'icbc', chimere_icbc)
Fields.register_plugin('LMDZ', 'ic', lmdz_ic)
