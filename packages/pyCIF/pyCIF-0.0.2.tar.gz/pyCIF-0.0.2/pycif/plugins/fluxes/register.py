#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lmdz_sflx
import lmdz_bin
import dummy_txt
import dummy_nc
import chimere
from pycif.utils.classes.fluxes import Fluxes

Fluxes.register_plugin('LMDZ', 'sflx', lmdz_sflx)
Fluxes.register_plugin('LMDZ', 'bin', lmdz_bin)
Fluxes.register_plugin('dummy', 'nc', dummy_nc)
Fluxes.register_plugin('dummy', 'txt', dummy_txt)
Fluxes.register_plugin('CHIMERE', 'AEMISSIONS', chimere)
