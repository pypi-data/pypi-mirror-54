from .run import run
from .native2inputs import native2inputs
from .outputs2native import outputs2native
from .ini_periods import ini_periods
import shutil
from types import MethodType
import pandas as pd
from pycif.utils import path
from pycif.utils.check import verbose

requirements = {'domain': {'name': 'CHIMERE', 'version': 'std',
                           'empty': False, 'any': False},
                'chemistry': {'name': 'CHIMERE', 'version': 'gasJtab',
                              'empty': False, 'any': False},
                'fluxes': {'name': 'CHIMERE', 'version': 'AEMISSIONS',
                           'empty': True, 'any': False},
                'meteo': {'name': 'CHIMERE', 'version': 'std',
                          'empty': False, 'any': False},
                'latcond': {'name': 'CHIMERE', 'version': 'icbc',
                            'empty': True, 'any': False, 'type': 'fields',
                            'newplg': True},
                'topcond': {'name': 'CHIMERE', 'version': 'icbc',
                            'empty': True, 'any': False, 'type': 'fields',
                            'newplg': True},
                'inicond': {'name': 'CHIMERE', 'version': 'icbc',
                            'empty': True, 'any': False, 'type': 'fields',
                            'newplg': True}}


def ini_data(plugin, **kwargs):
    """Initializes CHIMERE

    Args:
        plugin (dict): dictionary defining the plugin
        **kwargs (dictionary): possible extra parameters

    Returns:
        loaded plugin and directory with executable

    """
    
    verbose("Initializing the model")
    
    workdir = getattr(plugin, 'workdir', './')
    
    # Initializes the directory
    path.init_dir('{}/model'.format(workdir))
    
    # Copying the executables
    target = '{}/model/'.format(workdir)
    
    source = '{}/src/fwdchimere.e'.format(plugin.direxec)
    shutil.copy(source, target)
    
    source = '{}/src_tl/tlchimere.e'.format(plugin.direxec)
    shutil.copy(source, target)
    
    source = '{}/src_ad/achimere.e'.format(plugin.direxec)
    shutil.copy(source, target)
    
    # Required inputs for running a CHIMERE simulation
    plugin.required_inputs = ['exe', 'nml', 'fluxes',
                              'meteo', 'inicond', 'latcond', 'topcond']
    
    # Default values:
    # period: '1D'
    plugin.periods = getattr(plugin, 'periods', '1D')
    
    # Number of hours per period
    plugin.nhours = int(pd.to_timedelta(plugin.periods).total_seconds() / 3600)
    plugin.nho = '{:.0f}'.format(plugin.nhours)
    
    # Replace name for AEMISSION files
    plugin.fluxes.file = plugin.fluxes.file.format(nho=plugin.nho)

    # Replace name for BOUN_CONCS files
    plugin.latcond.file = plugin.latcond.file.format(nho=plugin.nho)
    plugin.topcond.file = plugin.topcond.file.format(nho=plugin.nho)

    return plugin
