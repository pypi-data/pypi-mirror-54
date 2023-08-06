#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import pycif.utils.check as check
from pycif.utils import path
from pycif.utils.check import verbose
from pycif.utils.netcdf import readnc


def fetch_meteo(meteo,
                datei,
                datef,
                workdir,
                **kwargs):
    """Fetch meteorology and links to the working directory

    Args:
        meteo (dictionary): dictionary defining the domain. Should include
        dirmeteo to be able to read the meteorology
        datei (datetime.datetime): initial date for the inversion window
        datef (datetime.datetime): end date for the inversion window
        workdir (str): path to the working directory where meteo files
                       should be copied
        logfile (str): path to the log file
        filetypes ([str]): list of file radicals to copy in the working
                           directory
        **kwargs (dictionary): extra arguments

    Return:
        None

    """
    
    check.verbose('Copying meteo files from ' + meteo.dirmeteo + ' to ' +
                  workdir + '/meteo/')
    
    # Create the sub-directory to store meteo files
    path.init_dir('{}/meteo/'.format(workdir))
    
    # Linking to file
    target = '{}/meteo/meteo.csv'.format(workdir)
    source = '{}/{}'.format(meteo.dirmeteo, meteo.filemeteo)

    try:
        path.link(source, target)

    except IOError:
        verbose('{} does not exist. Creating random meteo time series from given arguments'.format(source))
        meteo.create_meteo()
