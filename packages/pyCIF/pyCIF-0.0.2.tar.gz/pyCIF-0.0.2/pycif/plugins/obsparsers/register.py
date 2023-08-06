#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycif.utils.classes.obsparsers import ObsParser

import wdcgg

ObsParser.register_parser('WDCGG', 'std', wdcgg)
