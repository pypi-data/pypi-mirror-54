#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lmdz_massflx
import dummy_csv
import chimere_meteo
from pycif.utils.classes.meteos import Meteo

Meteo.register_plugin('LMDZ', 'mass-fluxes', lmdz_massflx)
Meteo.register_plugin('dummy', 'csv', dummy_csv)
Meteo.register_plugin('CHIMERE', 'std', chimere_meteo)