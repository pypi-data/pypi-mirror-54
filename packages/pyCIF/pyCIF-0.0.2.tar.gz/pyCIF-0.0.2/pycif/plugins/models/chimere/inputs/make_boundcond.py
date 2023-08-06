from pycif.utils import path
import os
import shutil
from netCDF4 import Dataset
import pandas as pd


def make_boundcond(self, datastore, runsubdir, sdc,
                   hour_dates, mode, input_type):
    """
    Generates boundary conditions files for CHIMERE

    :param self:
    :param datastore:
    :type datastore: dict
    :param runsubdir:
    :type runsubdir: str
    :param sdc:
    :type sdc: str
    :param hour_dates:
    :param mode:
    :param input_type:
    :return:
    """
    
    print "Deals with {}".format(input_type)
    
    # Name of variable in netCDF
    nc_varname = 'top_conc' if input_type == 'topcond' else 'lat_conc'
    
    # Fixed name for BC files
    fileout = '{}/BOUN_CONCS.nc'.format(runsubdir)
    fileoutincr = '{}/BOUN_CONCS.increment.nc'.format(runsubdir)
    
    # use ready-made BC files
    # Getting the right one
    nho = self.nho
    filein = self.boundcond.dir + 'BOUN_CONCS.{}.{}.nc'.format(sdc, nho)
    
    # Copy if not already initialized for other side (topcond or latcond)
    if not os.path.isfile(fileout):
        shutil.copy(filein, fileout)
    
    # If no species in the control vector, simply link the boundary
    # conditions
    if datastore == {}:
        with Dataset(fileout, 'a') as fout:
            with Dataset(filein, 'r') as fin:
                for k, spec in enumerate(self.chemistry.species['name']):
                    fout.variables[nc_varname][k, :] = \
                        fin.variables[nc_varname][k, :]
    
    # Otherwise, copy reference file and alter it if necessary
    # i.e., loop on active species and check if in control vector
    else:
        with Dataset(fileout, 'a') as f:
            nc_var = f.variables[nc_varname][:]
            for k, spec in enumerate(self.chemistry.species['name']):
                if spec in datastore:
                    # Apply to original data
                    nc_var[..., k] = datastore[spec]['spec'][:, :, 0, :]

            f.variables[nc_varname][:] = nc_var
    
    # the TL needs to also initialize the increments
    if mode == 'tl':
        if not os.path.isfile(fileoutincr):
            shutil.copy(filein, fileoutincr)
        
        with Dataset(fileoutincr, 'a') as f:
            nc_var = f.variables[nc_varname][:]
            for k, spec in enumerate(self.chemistry.species['name']):
                if spec not in datastore:
                    nc_var[..., k] = 0.
                else:
                    nc_var[..., k] = \
                        datastore[spec]['incr'][:, :, 0, :]

            f.variables[nc_varname][:] = nc_var
