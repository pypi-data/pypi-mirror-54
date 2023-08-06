import os
import shutil

from inputs.fluxes import *
from inputs.meteo import *
from pycif.utils import path
from pycif.utils.check import verbose
from pycif.utils.classes.baseclass import Plugin
from .flushrun import flushrun
from .ini_periods import ini_periods
from .inputs import make_input
from .native2inputs import native2inputs
from .outputs2native import outputs2native
from .run import run

requirements = {'domain': {'name': 'LMDZ', 'version': 'std', 'empty': False},
                'fluxes': {'name': 'LMDZ', 'version': 'bin', 'empty': True},
                'chemistry': {'name': 'CHIMERE', 'version': 'gasJtab',
                              'empty': False},
                'emis_species': {'name': 'LMDZ', 'version': 'sflx',
                                 'empty': True, 'type': 'fluxes'},
                'meteo': {'name': 'LMDZ', 'version': 'mass-fluxes',
                          'empty': False},
                'inicond': {'name': 'LMDZ', 'version': 'ic',
                            'empty': True, 'any': False, 'type': 'fields',
                            'newplg': True}}


def ini_data(plugin, **kwargs):
    """Initializes LMDZ
    
    Args:
        plugin (Plugin): the model plugin to initialize
        **kwargs (dictionary): possible extra parameters
        
    Returns:
        loaded plugin and directory with executable
        
    """
    
    verbose("Initializing the model")
    
    workdir = getattr(plugin, 'workdir', './')
    
    # Cleaning the model working directory
    shutil.rmtree('{}/model/'.format(workdir), ignore_errors=True)
    
    # Initializes the directory
    path.init_dir('{}/model'.format(workdir))
    
    # copying the executable
    target = '{}/model/'.format(workdir) + os.path.basename(plugin.fileexec)
    source = plugin.fileexec
    shutil.copy(source, target)
    
    # copying the definition file
    target = '{}/model/run.def'.format(workdir)
    source = plugin.filedef
    shutil.copy(source, target)
    
    # LMDZ has a fixed integration time step
    plugin.tstep = 0
    
    # Required inputs for running a LMDz simulations
    plugin.required_inputs = ['fluxes', 'meteo', 'inicond', 'def',
                              'chem_fields', 'prescrconcs', 'prodloss3d',
                              'traj']
    
    # Initializes default values
    # Period of sub-simulations: default = 1 month
    if not hasattr(plugin, 'periods'):
        plugin.periods = '1MS'
        
    # Convection scheme: default = TK = Tiedke
    if not hasattr(plugin, 'conv_scheme'):
        plugin.conv_scheme = 'TK'

    # Loading input fluxes if specified, otherwise, loads default inputs
    for spec in plugin.emis_species.attributes:
        tracer = getattr(plugin.emis_species, spec)
        
        if hasattr(tracer, 'provider') and hasattr(tracer, 'format'):
            name = tracer.provider
            version = tracer.format
        
        else:
            name = 'LMDZ'
            version = 'sflx'
        
        tracer.fluxes = Plugin.load_registered(name, version, 'fluxes',
                                               plg_orig=tracer)
    
    return plugin
