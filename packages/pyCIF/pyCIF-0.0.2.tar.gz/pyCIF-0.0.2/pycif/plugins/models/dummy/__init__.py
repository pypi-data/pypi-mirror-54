from .run import run
from .flushrun import flushrun
from .native2inputs import native2inputs
from .inputs import make_input
from .outputs2native import outputs2native
from .ini_periods import ini_periods

import os
import shutil

from pycif.utils import path
from pycif.utils.check import verbose
from pycif.utils.classes.baseclass import Plugin
from pycif.utils.classes.setup import Setup

requirements = {'domain': {'name': 'dummy', 'version': 'std', 'empty': False},
                'fluxes': {'name': 'dummy', 'version': 'nc', 'empty': True},
                'meteo': {'name': 'dummy', 'version': 'csv', 'empty': False}}


def ini_data(plugin, **kwargs):
    """Initializes the dummy_txt Gaussian model
    
    Args:
        plugin (Plugin): the model plugin to initialize
        **kwargs (dictionary): possible extra parameters
        
    Returns:
        loaded plugin and directory with executable
        
    """
    
    verbose("Initializing the model")
    
    workdir = getattr(plugin, 'workdir', './')
    
    # Initializes the directory
    path.init_dir('{}/model'.format(workdir))
    
    # copying the model Pasquill Gifford matrix
    target = '{}/model/'.format(workdir) + os.path.basename(plugin.file_pg)
    source = plugin.file_pg
    
    shutil.copy(source, target)
    
    # Required inputs for running a LMDz simulations
    plugin.required_inputs = ['fluxes', 'meteo', 'param']
    
    # Initializes default values:
    # - sub-simulations of 1day
    # - time steps of 1 hour
    plugin.periods = getattr(plugin, 'periods', '1D')
    plugin.tstep = getattr(plugin, 'tstep', '1H')
    plugin.save_H = getattr(plugin, 'save_H', False)

    plugin.H_matrix = {}
    
    return plugin
