#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pycif.utils.classes.platforms import Platform
import lsce_obelix

Platform.register_plugin('LSCE', 'obelix', lsce_obelix)
