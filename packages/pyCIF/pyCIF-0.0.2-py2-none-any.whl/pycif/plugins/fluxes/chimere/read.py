import pandas as pd
import pycif.utils.check as check
from pycif.utils import path
from pycif.utils.netcdf import readnc
import xarray as xr
import datetime
import numpy as np
import os


def read(self, name, tracdir, tracfile, dates,
         interpol_flx=False, **kwargs):
    """Get fluxes from pre-computed fluxes and load them into a pyCIF
    variables

    Args:
        self: the fluxes Plugin
        name: the name of the component
        tracdir, tracfile: flux directory and file format
        dates: list of dates to extract
        interpol_flx (bool): if True, interpolates fluxes at time t from
        values of surrounding available files

    """

    # Available files in the directory
    list_files = os.listdir(tracdir)
    list_available = []
    for flx_file in list_files:
        try:
            list_available.append(datetime.datetime.strptime(flx_file, tracfile))
        except:
            continue

    list_available = np.array(list_available)

    # Reading required fluxes files
    trcr_flx = []
    for dd in dates:
        delta = dd - list_available
        mask = delta >= datetime.timedelta(0)
        imin = np.argmin(delta[mask])
        fdates = list_available[mask][imin]

        filein = fdates.strftime('{}/{}'.format(tracdir, tracfile))

        data, times = readnc(filein, [name, 'Times'])

        # Get the correct hour in the file
        times = [datetime.datetime.strptime(''.join(s), '%Y-%m-%d_%H:%M:%S') for s in times]
        hour = int((dd - times[0]).total_seconds()) / 3600

        trcr_flx.append(data[hour, ...])
    
    # Building a xarray
    xmod = xr.DataArray(trcr_flx,
                        coords={'time': dates},
                        dims=('time', 'lev', 'lat', 'lon'))

    return xmod
