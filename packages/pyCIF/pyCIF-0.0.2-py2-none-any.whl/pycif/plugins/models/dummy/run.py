import subprocess
import datetime
import warnings
from pycif.utils import path
from pycif.utils import check
import os
import glob
import string
import calendar
import numpy as np
from pycif.utils.netcdf import save_nc
import pandas as pd
import xarray as xr


def run(self, runsubdir, mode, workdir,
        do_simu=True, **kwargs):
    """Run dummy_txt Gaussian model in forward or adjoint mode
    
    Args:
        runsubdir (str): working directory for the current run
        mode (str): forward or backward
        workdir (str): pycif working directory
        do_simu (bool): if False, considers that the simulation was
                        already run
    
    """
    # Ignore warnings in the toy model
    warnings.simplefilter("ignore")
    
    # Do the simulation
    if do_simu:
        
        # Linking Pasquill-Gifford classifileation
        source = '{}/model/Pasquill-Gifford.txt'.format(workdir)
        target = '{}/Pasquill-Gifford.txt'.format(runsubdir)
        path.link(source, target)
        
        # If H was already computed, take it from previous simulation
        check.verbose("Running the model Dummy in {}".format(runsubdir))
        dref = self.meteo.data.index.min()
        
        if dref in self.H_matrix:
            H = self.H_matrix[dref]
        
        else:
            H = fortran_exe(self, target, mode)
        
        # Saving H for later computations if required
        if self.save_H:
            self.H_matrix[dref] = H

        # Compute H.x or H^T.dy depending on the running mode
        meteo_index = self.dataobs['tstep']
        if mode in ['fwd', 'tl']:
            # In fwd and tl, simple product of flux and footprints
            self.dataobs['sim'] = \
                np.nansum(self.dataflx.values[meteo_index, 0] * H,
                          axis=(1, 2))
            self.dataobs['sim_tl'] = \
                np.nansum(self.dataflx_tl.values[meteo_index, 0] * H,
                          axis=(1, 2))

        else:
            # In adjoint, aggregation of footprints, to model resolution
            dflx = self.dataobs['obs_incr'][:, np.newaxis, np.newaxis] * H
            dflx[np.isnan(dflx)] = 0.

            dflx = xr.DataArray(dflx[:, np.newaxis],
                                coords={'time': meteo_index,
                                        'lev': [0],
                                        'lat': range(self.domain.nlat),
                                        'lon': range(self.domain.nlon)},
                                dims=('time', 'lev', 'lat', 'lon'))
    
            # Summing observations at the same hour and reprojecting to meteo
            # resolution if missing observations
            dflx = dflx.to_dataframe(name='flx') \
                .groupby(['time', 'lev', 'lat', 'lon']).sum()
            dflx = dflx.unstack(level=['lev', 'lat', 'lon'])
            dflx.index = self.meteo.data.index[dflx.index]
            dflx = dflx.reindex(self.meteo.data.index)\
                .stack(level=['lev', 'lat', 'lon'])
            dflx = xr.Dataset.from_dataframe(dflx)['flx']
    
            # Filling NaNs with 0, as it corresponds to hours with no obs
            dflx = dflx.fillna(0.)
    
            # Saving sensitivity to the model object
            # It corresponds to outputs in classical numerical models
            self.dflx = dflx
        
        
def fortran_exe(self, pg_file, mode):
    """Mimic the behaviour of a numerical model executable"""
    
    check.verbose("Running the 'FORTRAN' executable")
    
    # Loading Pasquill Gifford parameterization
    pg_params = pd.read_csv(pg_file)

    # Init variables
    meteo_index = self.dataobs['tstep']

    winddir = self.meteo.data['winddir']
    windspeed = self.meteo.data['windspeed']
    stabclass = self.meteo.data['stabclass']

    # Computing distance along plume in km
    dx = self.domain.zlon[np.newaxis] \
         - self.dataobs['lon'][:, np.newaxis, np.newaxis]
    dy = self.domain.zlat[np.newaxis] \
         - self.dataobs['lat'][:, np.newaxis, np.newaxis]
    dist = np.sqrt(dx ** 2 + dy ** 2) / 1e3

    theta = np.arctan2(dy, dx)
    y = dist \
        * np.cos(theta - np.radians(winddir.iloc[meteo_index]
                                    [:, np.newaxis, np.newaxis]))
    x = dist \
        * np.sin(theta - np.radians(winddir.iloc[meteo_index]
                                    [:, np.newaxis, np.newaxis]))

    x[x <= 0] = np.nan
    
    # y is needed in m in later formula
    y = np.abs(y) * 1e3
    
    # Select Pasquill-Gifford parameters
    mask = \
        (pg_params['xmin'][:, np.newaxis, np.newaxis, np.newaxis] <= x) \
        & (pg_params['xmax'][:, np.newaxis, np.newaxis, np.newaxis] >= x) \
        & (pg_params['Class'][:, np.newaxis, np.newaxis, np.newaxis]
           == stabclass.iloc[meteo_index][np.newaxis, :,
                                          np.newaxis, np.newaxis])
    inds = np.argmax(mask, axis=0)

    a = pg_params['a'].values[inds]
    b = pg_params['b'].values[inds]
    c = pg_params['c'].values[inds]
    d = pg_params['d'].values[inds]

    # Computing sigmas
    sigma_z = a * x ** b
    sigma_y = np.abs(465.11628 * x * np.tan(0.017653293 * (c - d * np.log(x))))
    
    # Cropping sigma values
    mask = (sigma_z > 5000.) \
           & (stabclass.iloc[meteo_index][:, np.newaxis, np.newaxis] < 'D')
    sigma_z[mask] = 5000.
    
    # Filling H matrix
    H = 1 / 2. / np.pi / sigma_y / sigma_z \
        / windspeed.iloc[meteo_index][:, np.newaxis, np.newaxis] \
        * np.exp(- y ** 2 / 2. / sigma_y ** 2) \
        * 2 * np.exp(- self.dataobs['alt'][:, np.newaxis, np.newaxis] ** 2
                     / 2. / sigma_z ** 2)
    H[np.isnan(H)] = 0.

    return H
