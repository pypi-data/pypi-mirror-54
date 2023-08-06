import calendar
import datetime
import glob
import os

import numpy as np
import pandas as pd

from pycif.utils.datastores.empty import init_empty


def outputs2native(self, runsubdir, mode='fwd', dump=True):
    """Reads outputs to pycif objects.
    
    If the mode is 'fwd' or 'tl', only observation-like outputs are extracted.
    For the 'adj' mode, all outputs relative to model sensitivity are extracted.
    
    Dumps to a NetCDF file with output concentrations if needed
    
    Args:
        self (pycif.utils.classes.models.Model): Model object
        runsubdir (str): current sub-sumilation directory
        mode (str): running mode; one of: 'fwd', 'tl', 'adj'; default is 'fwd'
        dump (bool): dumping outputs or not; default is True
    
    Return:
        dict
    
    """
    
    if not hasattr(self, 'dataobs'):
        self.dataobs = init_empty()
    
    if not hasattr(self, 'datasensit'):
        self.datasensit = {}
    
    if mode in ['tl', 'fwd']:
        # Read simulated concentrations
        sim_file = "{}/obs_out.bin".format(runsubdir)
        if not os.path.isfile(sim_file):
            self.dataobs.loc[:, 'sim'] = np.nan
            return
        
        with open(sim_file, 'rb') as f:
            sim = np.fromfile(f, dtype='float').reshape((-1, 4), order='F')

        # Observations that were not extracted by LMDZ are set to NaN
        sim[sim == 0] = np.nan

        # Putting values to the local data store
        self.dataobs.loc[:, 'sim'] = sim[:, 0]
        self.dataobs['pressure'] = sim[:, 2]
        self.dataobs['dp'] = sim[:, 3]
        
        if mode == 'tl':
            self.dataobs.loc[:, 'sim_tl'] = sim[:, 1]

        return self.dataobs
    
    elif mode == 'adj':
        nlon = self.domain.nlon
        nlat = self.domain.nlat
        
        # Stores daily dates of the period for later aggregation
        dref = datetime.datetime.strptime(
            os.path.basename(os.path.normpath(runsubdir)),
            "%Y-%m-%d_%H-%M")
        ndates = calendar.monthrange(dref.year, dref.month)[1]
        list_dates = \
            pd.date_range(dref, periods=ndates)
        
        # Puts data from binary outputs into self.data
        self.datasensit['adj_out'] = {'inicond': {}, 'fluxes': {},
                                      'prescrconcs': {}, 'prodloss3d': {}}
        
        list_file = glob.glob('{}/*_out.bin'.format(runsubdir))
        for out_file in list_file:
            with open(out_file, 'rb') as f:
                data = np.fromfile(f, dtype=np.float)
                data = data.reshape((nlon, nlat, -1), order='F') \
                    .transpose((2, 1, 0))
            
            if 'init' in out_file:
                spec = os.path.basename(out_file).split('_')[1]
                self.datasensit['adj_out']['inicond'][spec] = \
                    {'data': data[np.newaxis, ...], 'dates': np.array([dref])}

            elif 'prodscale' in out_file:
                spec = os.path.basename(out_file).split('_')[2]
                self.datasensit['adj_out']['prodloss3d'][spec] = \
                    {'data': data[:, np.newaxis, ...], 'dates': list_dates}
            
            elif 'scale' in out_file:
                spec = os.path.basename(out_file).split('_')[2]
                self.datasensit['adj_out']['prescrconcs'][spec] = \
                    {'data': data[:, np.newaxis, ...], 'dates': list_dates}
            
            elif 'mod' in out_file:
                spec = os.path.basename(out_file).split('_')[1]
                self.datasensit['adj_out']['fluxes'][spec] = \
                    {'data': data[:, np.newaxis, ...], 'dates': list_dates}
        
        return self.datasensit
