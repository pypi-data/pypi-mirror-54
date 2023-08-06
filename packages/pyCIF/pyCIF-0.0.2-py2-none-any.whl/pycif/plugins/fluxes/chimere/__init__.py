import os
from types import MethodType

from pycif.utils import path
from pycif.utils.check import verbose

from .read import read
from .write import write

requirements = {'domain': {'name': 'CHIMERE', 'version': 'std', 'empty': False},
                'chemistry': {'name': 'CHIMERE', 'version': 'gasJtab',
                              'empty': False}}


def ini_data(plugin, **kwargs):
    """Initializes the control vector from information in the Yaml file

    Args:
        plugin (pycif.classes.plugins): the plugin to initialize

    Return:
        - xb (explicitly and stored)
        - B (std and covariance definition), not stored
        - projectors and adjoints
        - product with B1/2


    """
    
    # Default file names for CHIMERE: AEMISSIONS
    if not hasattr(plugin, 'file'):
        plugin.file = 'AEMISSIONS.%Y%m%d%H.{nho}.nc'
