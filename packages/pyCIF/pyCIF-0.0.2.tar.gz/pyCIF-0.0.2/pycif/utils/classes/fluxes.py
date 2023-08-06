from types import MethodType

from .baseclass import Plugin
from pycif.utils.check.errclass import PluginError


class Fluxes(Plugin):
    
    @classmethod
    def register_plugin(cls, name, version, module, **kwargs):
        """Register a module for a plugin and version with possibly options

        Args:
            name (str):  name of the plugin
            version (str):  version of the plugin
            module (types.ModuleType): module defining the interface
                between pyCIF and the plugin
            plugin_type (str): type of plugin
            **kwargs (dictionary): default options for module

        """
        
        super(Fluxes, cls).register_plugin(name, version, module,
                                           plugin_type='fluxes')
    
    def read(self, name, tracdir, tracfile, dates, interpol_flx=False):
        """Get fluxes from pre-computed fluxes and load them into a pyCIF
        variables
    
        Args:
            self: the model Plugin
            name: the name of the component
            tracdir, tracfile: flux directory and file format
            dates: list of dates to extract
            interpol_flx (bool): if True, interpolates fluxes at time t from
            values of surrounding available files
    
        """
        raise PluginError('The function read was not defined')
    
    def write(self, flx_file, flx_fwd, flx_tl):
        """Write flux.
        
        Args:
            self (Fluxes): the Fluxes plugin
            flx_file (str): the file where to write fluxes
            flx_fwd, flx_tl: fluxes data to write
            """
        raise PluginError('The function write was not defined')
    
    def make(self, flx_file, flx_fwd, flx_tl):
        """Make fluxes.
        
        Args:
            self (Fluxes): the Fluxes plugin
            flx_file (str): the file where to write fluxes
            flx_fwd, flx_tl: fluxes data to write
            """
        raise PluginError('The function make was not defined')
    
    def initiate_template(self):
        module = super(Fluxes, self).initiate(plg_type='fluxes')
        
        # Replacing auxiliary functions:
        if hasattr(module, 'write'):
            self.write = MethodType(module.write, self)
        
        if hasattr(module, 'read'):
            self.read = MethodType(module.read, self)
        
        if hasattr(module, 'make'):
            self.make = MethodType(module.make, self)
