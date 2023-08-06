#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import pycif.utils.check as check
from pycif.utils import path
from pycif.utils.netcdf import readnc


def fetch_meteo(meteo,
                datei,
                datef,
                workdir,
                filetypes=['defstoke', 'fluxstoke', 'fluxstokev', 'phystoke'],
                **kwargs):
    """Reads meteorology and links to the working directory

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
        ????????

    Notes: At some point, include option to compute mass fluxes for LMDz,
    with different physics What is needed to do that? Possible only on CCRT?
    Flexibility to define new domains Can be very heavy and not necessarily
    relevant

    """
    
    check.verbose('Copying meteo files from ' + meteo.dirmeteo + ' to ' +
                  workdir + '/meteo/')
    
    # Create the sub-directory to store meteo files
    path.init_dir('{}/meteo/'.format(workdir))
    
    # Loop over dates and file types
    date_range = pd.date_range(datei, datef, freq='1M')
    
    for date in date_range:
        for filetype in filetypes:
            meteo_file = "{}.an{}.m{:02d}.nc".format(filetype,
                                              date.year, date.month)
            
            if (filetype == 'defstoke'
                    and not os.path.isfile(meteo.dirmeteo + meteo_file)):
                meteo_file = filetype + '.nc'
            
            target = '{}/meteo/{}'.format(workdir, meteo_file)
            source = '{}/{}'.format(meteo.dirmeteo, meteo_file)
            path.link(source, target)
