from .minimize import minimize
from .check import check_options
from .opt import m1qn3
from .aux import mlis0
from types import MethodType

requirements = {'simulator': {'any': True, 'empty': True,
                              'name': 'gausscost', 'version': 'std'},
                }


def ini_data(plugin, **kwargs):
    """Initializes M1QN3.

    Args:
        plugin (Plugin): options for the variational inversion

    Returns:
        updated plugin

    """
    
    # Function to check the consistency of options and arguments
    plugin.check_options = MethodType(check_options, plugin)
    
    # M1QN3 itself
    plugin.m1qn3 = MethodType(m1qn3, plugin)
    plugin.mlis0 = MethodType(mlis0, plugin)
    
    return plugin
