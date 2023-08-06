import pandas as pd
import pycif.utils.check as check
from pycif.utils import path
import xarray as xr
import datetime
import numpy as np


def read(self, name, tracdir, tracfile, dates,
                interpol_flx=False, **kwargs):
    """Get fluxes from pre-computed fluxes and load them into a pycif
    variables

    Args:
        self: the model Plugin
        name: the name of the component
        tracdir, tracfile: flux directory and file format
        dates: list of dates to extract
        interpol_flx (bool): if True, interpolates fluxes at time t from
        values of surrounding available files

    """

    list_file_flx = [dd.strftime(tracfile)
                    for dd in dates]
    
    # Reading fluxes for periods within the simulation window
    trcr_flx = []
    for dd, file_flx in zip(dates, list_file_flx):
        flx_file = '{}/{}'.format(tracdir, file_flx)
        try:
            flx = np.loadtxt(flx_file, delimiter=',')
        
        except IOError:
            check.verbose('Fluxes are not available in {}. \n'
                          'Creating them from text'.format(flx_file))
            flx = self.make(flx_file, self.flx_text)
    
        # Checking the fluxes shape
        nlat = self.domain.nlat
        nlon = self.domain.nlon

        if flx.shape[1:] != (nlat, nlon):
            raise Exception("Fluxes of shape {} are not consistent "
                            "with the domain definition {}/{}"
                            .format(flx.shape, nlat, nlon))
        
        # Appending to list
        trcr_flx.append(flx)
    
    # Putting fluxes to an xarray
    xmod = xr.DataArray(trcr_flx,
                        coords={'time': dates},
                        dims=('time', 'lev', 'lat', 'lon'))

    return xmod
