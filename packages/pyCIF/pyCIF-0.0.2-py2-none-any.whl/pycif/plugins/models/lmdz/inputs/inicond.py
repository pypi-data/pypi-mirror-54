from scipy.io import FortranFile
import numpy as np
from pycif.utils import path
import shutil
from netCDF4 import Dataset


def make_inicond(self, datastore, datei, datef, runsubdir, mode):

    ddi = min(datei, datef)
    ddf = max(datei, datef)
    
    # Reference initial condition file for looping sub-simulations
    if hasattr(self, 'chain'):
        source = self.chain.strftime(
            "{}/../chain/restart_%Y%m%d%H%M.nc".format(runsubdir))
        target = "{}/start.nc".format(runsubdir)
        path.link(source, target)
        
        if mode == 'tl':
            source = self.chain.strftime(
                "{}/../chain/restart_tl_%Y%m%d%H%M.bin".format(runsubdir))
            target = "{}/start_tl.bin".format(runsubdir)
            path.link(source, target)
        
        return
    
    # Generating reference initial conditions if first sub-simulation
    source = ddi.strftime(
        "{}/{}".format(self.inicond.dir,
                       self.inicond.file))
    target = "{}/start.nc".format(runsubdir)
    shutil.copy(source, target)
    if mode in ['fwd', 'tl'] and ddi == self.datei:
        with Dataset(target, 'a') as f:
            for spec in self.chemistry.acspecies.attributes:
                restartID = \
                    getattr(self.chemistry.acspecies, spec).restart_id
                if spec in datastore:
                    data = datastore[spec]
                    var = 'q{:02d}'.format(restartID)
                    if var in f.variables:
                        inicond = data['spec'].values
                        f.variables[var][:] = inicond

        if mode == 'tl':
            target = "{}/start_tl.nc".format(runsubdir)
            shutil.copy(source, target)
            with Dataset(target, 'a') as f:
                for spec in self.chemistry.acspecies.attributes:
                    restartID = \
                        getattr(self.chemistry.acspecies, spec).restart_id
                    var = 'q{:02d}'.format(restartID)
                    if var in f.variables:
                        inicond = 0.
                        if spec in datastore:
                            data = datastore[spec]
                            if 'incr' in data:
                                inicond = data['incr'].values
                            else:
                                inicond = 0. * data['spec'].values
                        f.variables[var][:] = inicond

    elif mode == 'adj' and ddf == self.datef:
        for spec in self.chemistry.acspecies.attributes:
            restartID = \
                getattr(self.chemistry.acspecies, spec).restart_id
            with Dataset(target, 'a') as f:
                var = 'q{:02d}'.format(restartID)
                if var in f.variables:
                    f.variables[var][:] = 0.