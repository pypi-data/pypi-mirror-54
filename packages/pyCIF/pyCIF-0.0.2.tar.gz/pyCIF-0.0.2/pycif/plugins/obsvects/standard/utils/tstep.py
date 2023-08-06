import pandas as pd
import numpy as np
from copy import deepcopy
from itertools import count, izip
from pycif.utils.check import verbose


def tstep(obsvect, **kwargs):
    """Computes the time steps corresponding to observations in the model.
    
    """
    
    verbose("Finding model time steps corresponding to observations")
    
    # Don't do anything if the datastore is empty
    if len(obsvect.datastore) == 0:
        return obsvect
    
    # Initialize variables
    model = obsvect.model
    datei = obsvect.datei
    datef = obsvect.datef
    
    subsimu_dates = model.subsimu_dates
    tstep_dates = model.tstep_dates
    
    # Add datef for obs ending right at the end of the period
    tstep_all = model.tstep_all
    
    # Computing timestep
    ds = obsvect.datastore
    
    ds.loc[:, 'tstep'] = -1
    ds.loc[:, 'dtstep'] = -1
    
    # Looping over sub-periods to set date reference for tstep as the start
    # of each sub-simulation
    for ddi, ddf \
            in zip(subsimu_dates[:-1], subsimu_dates[1:]):
        verbose('Processing time steps for observations from {} to {}'
                .format(ddi, ddf))
        
        mask = (ds.index >= ddi) \
               & (ds.index < ddf)
        
        tsteps = tstep_dates[ddi]
        
        # Use an intermediate dataframe to find indexes
        # corresponding to time steps
        df_tsteps = pd.DataFrame(data=range(len(tsteps)), index=tsteps)

        ds.loc[mask, 'tstep'] = \
            df_tsteps.reindex(ds.loc[mask].index, method='ffill').values
    
    # Computing number of time steps for each observation
    df_steps = pd.DataFrame(data=range(len(tstep_all)), index=tstep_all)
    df_isteps = df_steps.reindex(ds.index, method='ffill')
    df_esteps = df_steps.reindex(ds.index
                                 + pd.to_timedelta(ds['duration'], unit='h'),
                                 method='bfill')
    
    ds.loc[:, 'dtstep'] = df_esteps.values - df_isteps.values
    ds.loc[:, 'tstep_glo'] = df_isteps.values
    
    # Change type to integer
    ds.loc[~np.isnan(ds['tstep']), 'tstep'] = \
        ds['tstep'][~np.isnan(ds['tstep'])].astype(int)
    ds.loc[~np.isnan(ds['dtstep']), 'dtstep'] = \
        ds['dtstep'][~np.isnan(ds['dtstep'])].astype(int)
    ds.loc[~np.isnan(ds['tstep_glo']), 'tstep_glo'] = \
        ds['tstep_glo'][~np.isnan(ds['tstep_glo'])].astype(int)
    
    return obsvect
