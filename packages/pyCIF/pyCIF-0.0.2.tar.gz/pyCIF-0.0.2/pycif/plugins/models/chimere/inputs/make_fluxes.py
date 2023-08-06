from pycif.utils import path
import shutil
import pandas as pd

from netCDF4 import Dataset
import xarray as xr


def make_fluxes(self, datastore, runsubdir, datei, mode):
    """Make AEMISSIONS.nc and BEMISSIONS.nc files for CHIMERE.
    Use chemical scheme to check which species is needed and either take it
    from the datastore (i.e. when defined in the control vector), or take it
    from prescribed emissions
    
    Args:
        self (pycif.utils.classes.Fluxes.fluxes): Flux plugin with all
                    attributes
        datastore (dict): information on flux species
        runsubdir (str): directory to the current run
        nho (int): number of hours in the run
        mode (str): running mode: 'fwd', 'tl' or 'adj'
    
    """
    
    print " Deals with fluxes"
    
    # Fixed name for AEMISSIONS files
    file_emisout = '{}/AEMISSIONS.nc'.format(runsubdir)
    file_emisincrout = '{}/AEMISSIONS.increment.nc'.format(runsubdir)
    
    # List of dates for which emissions are needed
    list_dates = pd.date_range(datei, periods=self.nhours + 1, freq='H')
    
    # Getting the right emissions
    if datastore == {}:
        fileemis = datei.strftime('{}/{}'.format(self.fluxes.dir,
                                                self.fluxes.file))
        path.link(fileemis, file_emisout)
        
        if mode == 'tl':
            shutil.copy(fileemis, file_emisincrout)
            with Dataset(file_emisincrout, 'a') as f:
                for spec in self.chemistry.species['name']:
                    f.variables[spec][:] = 0.
    
    else:
        # Loop on all anthropogenic species
        # If in datastore, take data, otherwise, link to original AEMISSIONS
        for spec in self.chemistry.anthro_species['name']:
            if spec not in datastore:
                fileorig = datastore['CH4']['fileorig']
                dirorig = datastore['CH4']['dirorig']
                
                fileemis = datei.strftime(fileorig)
                flx_fwd = self.fluxes.read(spec, dirorig, fileemis, list_dates)
                flx_tl = 0. * flx_fwd
            
            else:
                flx_fwd = datastore[spec]['spec']
                flx_tl = datastore[spec].get('incr', 0. * flx_fwd)

            # Put in dataset and write to input
            self.fluxes.write(spec, file_emisout, flx_fwd)
            
            if mode == 'tl':
                self.fluxes.write(spec, file_emisincrout, flx_tl)
                





