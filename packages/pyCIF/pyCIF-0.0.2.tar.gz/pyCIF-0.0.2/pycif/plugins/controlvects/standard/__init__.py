from .init_xb import init_xb
from .init_bprod import init_bprod
from .control2native import control2native
from .native2control import native2control
from .sqrtbprod import sqrtbprod, sqrtbprod_ad
from .dump import dump, load
from pycif.utils.path import init_dir
from pycif.utils.check.errclass import PluginError

# It is necessary to initialize a domain, fluxes and the model itself
requirements = {'domain': {'any': True, 'empty': False},
                'model': {'any': True, 'empty': False},
                'components': {'any': True, 'empty': True, 'type': 'fields'}
                }


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
    # Initializes reference directories if needed
    init_dir('{}/controlvect/'.format(plugin.workdir))
    
    # Saves reference directories and file formats if not prescribed
    # Look for directory by order of priority:
    # 1) directly in tracer definition
    # 2) in component definition if specified
    # 3) in model fluxes if any
    # Getting the right emissions
    if hasattr(plugin, 'components'):
        components = plugin.components
        for comp in components.attributes:
            component = getattr(components, comp)
            for trcr in component.parameters.attributes:
                tracer = getattr(component.parameters, trcr)

                tracer.dir = getattr(tracer, 'dir',
                                     getattr(component, 'dir',
                                             getattr(
                                                 getattr(plugin.model,
                                                         comp, None),
                                                 'dir', '')))
                tracer.file = getattr(tracer, 'file',
                                     getattr(component, 'file',
                                             getattr(
                                                 getattr(plugin.model,
                                                         comp, None),
                                                 'file', '')))
                
                # Forces the tracer to have an empty read function
                if not hasattr(tracer, 'read'):
                    tracer = tracer.get_subclass('fields')(plg_orig=tracer)
                    setattr(component.parameters, trcr, tracer)

                # Gets read from model if not already defined
                try:
                    tracer.read(*range(4))
                except PluginError:
                    if comp in ['fluxes', 'inicond', 'latcond', 'topcond']:
                        tracer.read = getattr(plugin.model, comp).read

                    else:
                        raise Exception('WARNING: {} was not defined in the '
                                        'accepted components types of the '
                                        'control vector'.format(comp))

                except Exception:
                    pass

                # Gets the domain and
                # change it the domain side if lateral conditions
                if comp == 'latcond':
                    tracer.domain = plugin.domain.get_sides()

                else:
                    tracer.domain = plugin.domain

    # Initializing xb with its original values
    init_xb(plugin, **kwargs)
    
    # Initializing the product of chi by B^(1/2), only if components specified
    if hasattr(plugin, 'components'):
        init_bprod(plugin, **kwargs)
