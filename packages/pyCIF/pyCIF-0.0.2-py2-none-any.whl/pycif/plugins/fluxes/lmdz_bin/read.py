import pandas as pd
import pycif.utils.check as check
from pycif.utils import path
import xarray as xr
import datetime
import numpy as np
from scipy.io import FortranFile


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
    
    trcr_dates = []
    trcr_flx = []
    trcr_flx_tl = []
    for dd, file_flx in zip(dates, list_file_flx):
        # Read binary file
        data = []
        
        with FortranFile('{}/{}'.format(tracdir, file_flx)) as f:
            while True:
                try:
                    data.append(f.read_reals())
                
                except:
                    check.verbose('End of file {}'.format(file_flx))
                    break
        
        # Reshape file
        nlon = self.domain.nlon
        nlat = self.domain.nlat
        
        data = np.array(data)
        
        flx = data[:, 0].reshape((-1, nlat, nlon))
        flx_tl = data[:, 1].reshape((-1, nlat, nlon))
        
        trcr_flx.append(flx)
        trcr_flx_tl.append(flx_tl)
        trcr_dates.extend(list(pd.date_range(dd, freq='D', periods=len(flx))))
    
    xmod = xr.DataArray(trcr_flx[0],
                        coords={'time': trcr_dates},
                        dims=('time', 'lat', 'lon'))
    
    return xmod
