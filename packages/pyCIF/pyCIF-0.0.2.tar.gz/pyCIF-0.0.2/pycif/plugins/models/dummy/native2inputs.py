from scipy.io import FortranFile
import numpy as np
import xarray as xr
import calendar
import os
import string
from netCDF4 import Dataset
import pandas as pd
from pycif.utils import path


def native2inputs(self, datastore, input_type, datei, datef, mode,
                  runsubdir, workdir):
    """Converts data at the model data resolution to model compatible input
    files.
    
    Args:
        self: the model Plugin
        input_type (str): one of 'fluxes', 'obs'
        datastore: data to convert
            if input_type == 'fluxes', a dictionary with flux maps
            if input_type == 'obs', a pandas dataframe with the observations
        datei, datef: date interval of the sub-simulation
        mode (str): running mode: one of 'fwd', 'adj' and 'tl'
        runsubdir (str): sub-directory for the current simulation
        workdir (str): the directory of the whole pycif simulation
    
    Notes:
        - LMDZ expects daily inputs; if the periods in the control vector are
        longer than one day, period values are uniformly de-aggregated to the
        daily scale; this is done with pandas function 'asfreq' and the option
        'ffill' as 'forward-filling'
        See Pandas page for details:
        https://pandas.pydata.org/pandas-docs/stable/generated/pandas
        .DataFrame.asfreq.html
        
    """
    
    if datastore is None:
        datastore = {}
    
    # Switching datei and datef if adj
    ddi = min(datei, datef)
    ddf = max(datei, datef)
    
    # Deals with fluxes
    if input_type == 'fluxes':
        for spec in datastore:
            flx = datastore[spec]['spec']
            
            if 'scale' in datastore[spec]:
                flx *= datastore[spec]['scale']
            
            # Keeping only data in the simulation window
            mask = (flx.time >= np.datetime64(ddi)) \
                   & (flx.time <= np.datetime64(ddf))
            mask = np.where(mask)[0]
            
            flx_fwd = flx[mask]
            flx_tl = 0. * flx_fwd
            if 'incr' in datastore[spec]:
                flx_tl = datastore[spec]['incr'][mask]

            # Saving data in model object
            # For other models, intermediate NetCDF or binary files should be
            # saved for later use by numerical Fortran (or other) model
            self.dataflx = flx_fwd
            self.dataflx_tl = flx_tl
            
    # Deals with observations
    elif input_type == 'obs':
        # If empty datastore, do nothing
        if datastore.size == 0:
            return

        # Otherwise, unfold observations spanning several time steps
        dataobs = datastore.loc[
            datastore.index.repeat(datastore['dtstep'])]
        dataobs.loc[:, 'tstep'] = \
            dataobs.groupby([dataobs.index, 'station', 'i', 'j'])['tstep']\
                .transform(lambda x: np.arange(x[0], x[0] + len(x)))

        # Saves the data to the model
        # Other models might need an input file to be writen here to get info
        #  on observations
        self.dataobs = dataobs
        
    # Deals with meteo
    elif input_type == 'meteo':
        ddi = min(datei, datef)
        ddf = max(datei, datef)
        self.meteo.read_meteo(ddi, ddf, workdir)
    
    return
