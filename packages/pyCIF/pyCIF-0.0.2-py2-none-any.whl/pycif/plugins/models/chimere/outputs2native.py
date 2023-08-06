import numpy as np
import os
import glob
import pandas as pd
import datetime
from netCDF4 import Dataset
from pycif.utils.check import verbose
from pycif.utils.datastores.empty import init_empty


def outputs2native(self, runsubdir, mode='fwd', dump=True):
    """Reads outputs to pyCIF objects.

    If the mode is 'fwd' or 'tl', only onservation-like outputs are extracted.
    For the 'adj' mode, all outputs relative to model sensitivity are extracted.

    Dumps to a NetCDF file with output concentrations if needed"""
    
    if not hasattr(self, 'dataobs'):
        self.dataobs = init_empty()
    
    if not hasattr(self, 'datasensit'):
        self.datasensit = {}
  
    if mode in ['fwd', 'tl']:
        # If no simulated concentration is available just pass
        sim_file = "{}/mod.txt".format(runsubdir)
        if os.stat(sim_file).st_size == 0:
            verbose("CHIMERE ran without any observation to be compared with for sub-simu "
            "only CHIMERE's outputs are available")
            self.dataobs.loc[:, 'sim'] = np.nan
            return
        
        # Read simulated concentrations
        sim = pd.read_csv(sim_file, sep='\s+', header=None)[6]
        
        # Loop over observations in active species
        mask = self.dataobs['parameter'].str.upper() \
            .isin(list(self.chemistry.species['name']))

        # Putting values to the local data store
        # Assumes arithmetic averages upto now
        inds = [0] + list(np.cumsum(self.dataobs.loc[mask, 'dtstep'][:-1]))
        
        column = 'sim' if mode == 'fwd' else 'sim_tl'
        self.dataobs.loc[mask, column] = \
            [sim.iloc[k:k + dt].sum()
             for k, dt in zip(inds, self.dataobs.loc[mask, 'dtstep'])]
        
        return self.dataobs
        
    elif mode == 'adj':
        # List of CHIMERE dates
        # TODO: include these dates in ini_periods once for all
        dref = datetime.datetime.strptime(
            os.path.basename(os.path.normpath(runsubdir)),
            "%Y-%m-%d_%H-%M")
        list_dates = \
            pd.date_range(dref, periods=self.nhours + 1, freq='1H')
        # Puts data from binary outputs into self.data
        self.datasensit['adj_out'] = {'inicond': {}, 'fluxes': {},
                                      'latcond': {}, 'topcond': {}}
        
        list_file = glob.glob('{}/aout.*.nc'.format(runsubdir))
        for out_file in list_file:
            with Dataset(out_file, 'r') as f:
                # Load list of species and reformat it
                list_species = [''.join(s).strip() 
                                for s in f.variables['species'][:]]             

                if 'ini' in out_file or 'aemis' in out_file:
                    data = {s: f.variables[s][:] for s in list_species}
                
                elif 'bc' in out_file:
                    data_lat = {s: f.variables['lat_conc'][..., k]
                                for k, s in enumerate(list_species)}
                    data_top = {s: f.variables['top_conc'][..., k]
                                for k, s in enumerate(list_species)}
            
            if 'ini' in out_file:
                for spec in data:
                    self.datasensit['adj_out']['inicond'][spec] = \
                        {'data': data[spec][np.newaxis, ...],
                         'dates': np.array([dref])}
            
            elif 'bc' in out_file:
                for spec in data_lat:
                    self.datasensit['adj_out']['latcond'][spec] = \
                        {'data': data_lat[spec][..., np.newaxis, :],
                         'dates': list_dates}
                
                for spec in data_top:
                    self.datasensit['adj_out']['topcond'][spec] = \
                        {'data': data_top[spec][:, np.newaxis, ...],
                         'dates': list_dates}
            
            elif 'aemis' in out_file:
                for spec in data:
                    self.datasensit['adj_out']['fluxes'][spec] = \
                        {'data': data[spec], 'dates': list_dates}
    
    return self.datasensit
