from types import MethodType

from .baseclass import Plugin
from pycif.utils.check import verbose


class ControlVect(Plugin):
    
    def initiate_template(self):
        module = super(ControlVect, self).initiate(plg_type='controlvect')
        
        # Replacing auxiliary functions:
        # Need some function to convert information from the control space
        # to the space of native model resolution
        if hasattr(module, 'control2native'):
            self.control2native = MethodType(module.control2native, self)
        
        if hasattr(module, 'native2control'):
            self.native2control = MethodType(module.native2control, self)
        
        # Define how to multiple by sqrt-B, i.e. translating information
        # from the minimization space to the physical space
        if hasattr(module, 'sqrtbprod'):
            self.sqrtbprod = MethodType(module.sqrtbprod, self)
        
        if hasattr(module, 'sqrtbprod_ad'):
            self.sqrtbprod_ad = MethodType(module.sqrtbprod_ad, self)
        
        # Load and dump control vectors
        if hasattr(module, 'dump'):
            self.dump = MethodType(module.dump, self)
        
        if hasattr(module, 'load'):
            self.load = MethodType(module.load, self)
    
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
        
        super(ControlVect, cls).register_plugin(name, version, module,
                                                plugin_type='controlvect')
