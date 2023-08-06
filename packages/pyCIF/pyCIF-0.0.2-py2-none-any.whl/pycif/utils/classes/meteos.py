from types import MethodType

from .baseclass import Plugin
from pycif.utils.check.errclass import PluginError
from pycif.utils import check


class Meteo(Plugin):
    
    def initiate_template(self):
        module = super(Meteo, self).initiate(plg_type='meteo')
        
        # Replacing auxiliary functions:
        if hasattr(module, 'read_meteo'):
            self.read_meteo = MethodType(module.read_meteo, self)
        
        if hasattr(module, 'create_meteo'):
            self.create_meteo = MethodType(module.create_meteo, self)
        
        if hasattr(module, 'fetch_meteo'):
            self.fetch_meteo = MethodType(module.fetch_meteo, self)
    
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
        
        super(Meteo, cls).register_plugin(name, version, module,
                                          plugin_type='meteo')
    
    def create_meteo(self,
                   datei,
                   datef,
                   workdir,
                   logfile=None,
                   **kwargs):
        """Creates meteo files if necessary

        Args:
            meteo (dictionary): dictionary defining the domain. Should include
            dirmeteo to be able to read the meteorology
            datei (datetime.datetime): initial date for the inversion window
            datef (datetime.datetime): end date for the inversion window
            logfile (str): path to the log file

        Returns:
             Error as LMDZ shouldn't be used without pre-computed meteorology

        """
        
        raise PluginError("The computation of meteo files is not defined!")
