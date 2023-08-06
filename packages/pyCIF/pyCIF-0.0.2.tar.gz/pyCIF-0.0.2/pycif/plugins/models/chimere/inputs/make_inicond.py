from pycif.utils import path
import shutil
from netCDF4 import Dataset
import numpy as np


def make_inicond(self, datastore, runsubdir, mode, datef):
    print "Deals with inicond"
    # Fixed name for INI_CONCS files
    fileout = '{}/INI_CONCS.0.nc'.format(runsubdir)
    fileoutincr = '{}/INI_CONCS.0.increment.nc'.format(runsubdir)
    nho = self.nho
    
    print "Use ready-made INI_CONCS.nc file", mode
    # Getting the right one
    # if chained period
    if mode in ['tl', 'fwd']:
        if hasattr(self, 'chain'):
            filein = self.chain.strftime(
                "{}/../chain/end.%Y%m%d%H.{}.nc".format(runsubdir, nho))
            path.link(filein, fileout)
        
        else:
            # For the first period
            filein = '{}/{}'.format(self.inicond.dir, self.inicond.file)
            
            # If no species in the control vector, simply link the initial
            # conditions
            if datastore == {}:
                path.link(filein, fileout)
            
            # Otherwise, copy reference file and alter it if necessary
            # i.e., loop on active species and check if in control vector
            else:
                shutil.copy(filein, fileout)
                with Dataset(fileout, 'a') as f:
                    for spec in self.chemistry.species['name']:
                        if spec in datastore:
                            f.variables[spec][:] = datastore[spec]['spec']
            
            # the TL needs to also initialize the increments
            if mode == 'tl':
                shutil.copy(filein, fileoutincr)
                with Dataset(fileoutincr, 'a') as f:
                    for spec in self.chemistry.species['name']:
                        if spec not in datastore:
                            f.variables[spec][:] = 0.
                        else:
                            f.variables[spec][:] = datastore[spec]['incr']
    
    else:
        # For the first period
        if datef == self.datei:
            filein = '{}/{}'.format(self.inicond.dir, self.inicond.file)
        
        else:
            subsimu_dates = self.subsimu_dates
            date_index = np.where(subsimu_dates == datef)[0][0]
            refdir = self.adj_refdir
            filein = subsimu_dates[date_index - 1].strftime(
                "{}/chain/end.%Y%m%d%H.{}.nc".format(refdir, nho))
        
        path.link(filein, fileout)
    
    # The adjoint needs to chain also sensitivities
    if mode == 'adj':
        if hasattr(self, 'chain'):
            filein = self.chain.strftime(
                "{}/../chain/aend.%Y%m%d%H.{}.nc".format(runsubdir, nho))
            fileout = self.chain.strftime(
                "{}/aini.nc".format(runsubdir))
            path.link(filein, fileout)
