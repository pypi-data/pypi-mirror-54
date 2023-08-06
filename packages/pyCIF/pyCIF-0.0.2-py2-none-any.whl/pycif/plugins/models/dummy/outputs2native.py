import numpy as np
import datetime
import os
import calendar
import glob
import pandas as pd

from pycif.utils.netcdf import save_nc
from pycif.utils.check import verbose


def outputs2native(self, runsubdir, mode='fwd', dump=True):
    """Reads outputs to pycif objects.
    
    If the mode is 'fwd' or 'tl', only onservation-like outputs are extracted.
    For the 'adj' mode, all outputs relative to model sensitivity are extracted.
    
    Dumps to a NetCDF file with output concentrations if needed"""
    
    if not hasattr(self, 'dataobs'):
        self.dataobs = pd.DataFrame({})
    
    if not hasattr(self, 'datasensit'):
        self.datasensit = {}
    
    if mode in ['tl', 'fwd']:
        # Read simulated concentrations
        # In classical model, this should correspond to reading output files
        # Here the observations are already stored in the model object
        datastore = self.dataobs
        
        # Re-aggregate observations spanning several time steps
        # Obsvect divides by number of tstep at higher level
        # (in case the observation spans several periods)
        ds = datastore.groupby([datastore.index, 'station', 'i', 'j']).sum()
        ds = ds[['sim', 'sim_tl']]
        ds.index = ds.index.get_level_values(0)
        
        self.dataobs = ds
    
    elif mode == 'adj':
        # Reads sensitivities
        # In the toy model's case, just take the data from the object itself
        datasensit = self.dflx
        
        # Putting the sensitivities to a dictionary
        self.datasensit['adj_out'] = \
            {'fluxes': {}}
        self.datasensit['adj_out']['fluxes']['CH4'] = \
            {'data': datasensit.values,
             'dates': pd.to_datetime(datasensit.date.values)}
        
        return self.datasensit
