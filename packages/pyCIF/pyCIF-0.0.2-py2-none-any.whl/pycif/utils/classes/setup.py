from types import MethodType
import copy
import yaml
import os
import pycif.utils.check as check
import pycif.utils.dates as dates
from pycif.utils.check.errclass import PluginError

from .baseclass import Plugin
from pycif.utils.check import verbose
from pycif.utils.check import init_log, error, verbose
from pycif.utils.yml import ordered_load


class Setup(Plugin):

    @classmethod
    def run_simu(cls, args):

        setup = cls.load_config(args['def_file'])

        # Copying Yaml file for traceability of simulations
        os.system('cp ' + setup.def_file
                  + ' ' + setup.workdir + '/')

        # Run the mode
        if getattr(getattr(setup, 'mode', None), 'loaded_requirements', False):
            return setup.mode.execute(**args)
        
        else:
            verbose('pycif has correctly been initialized '
                    'but no execution mode was specified')

    @classmethod
    def load_config(cls, config_file):

        # TODO: Allow for anothere type of files than yaml?
        config_dict = cls.from_yaml(config_file)

        # Creates and initializes the log file
        config_dict['logfile'], config_dict['workdir'] \
            = init_log(config_dict['logfile'],
                       config_dict['workdir'],
                       config_dict['verbose'])
        cls.config_verbose(config_dict)

        # Looking for others Yaml configs files in the main config_file
        config_dict = cls.yaml_subconfigs(config_dict)

        # Load a dictionary to a Setup recursive object
        setup = Setup.from_dict(config_dict)

        # Initialize every plugin, requirements and data
        cls.load_setup(setup, level=0)

        return setup

    @classmethod
    def from_yaml(cls, def_file):
        """Generates a dictionary including all pyCIF parameters
        
        Args:
            def_file (string) : Path to the definition file
                                Handles both absolute and relative paths
    
        Returns:
            config_dict (dictionary): Dictionary populated with all pyCIF
            parameters
    
        """
        
        yml_file = os.path.abspath(os.path.expanduser(def_file))
        
        try:
            with open(yml_file, 'r') as f:
                config_dict = ordered_load(f)
                
                config_dict['def_file'] = yml_file
                
                # Converting dates to datetime if necessary
                config_dict['datei'] = dates.date2datetime(config_dict['datei'])
                config_dict['datef'] = dates.date2datetime(config_dict['datef'])
                
                return config_dict
        
        except IOError as e:
            verbose("Couldn't find config file: {}".format(yml_file))
            verbose("Please check directories")
            raise e
        
        except yaml.scanner.ScannerError as e:
            verbose("Error in the syntax of config file: {}".format(yml_file))
            raise e

    @classmethod
    def yaml_subconfigs(cls, config_dict):
        for key, value in config_dict.iteritems():
            if isinstance(value, dict):
                config_dict[key] = cls.yaml_subconfigs(value)
            else:
                if key == 'file_yaml':
                    if not os.path.isfile(value):
                        raise OSError('The Yaml path given is not a file : '
                                      '{}'.format(value))
                    if not os.path.exists(value):
                        raise OSError('The Yaml path given is not valid '
                                      '{}'.format(value))
                    with open(value, 'r') as f:
                        subconfig_dict = yaml.load(f)
                        config_dict = subconfig_dict
        return config_dict

    @classmethod
    def config_verbose(cls, config_dict):
        """Prints out main input parameters for pyCIF
        """
        
        verbose_txt = [
            "pyCIF has been initialized with the following parameters:",
            "Yaml configuration file: {}".format(config_dict['def_file']),
            "Log file: {}".format(config_dict['logfile']),
            "Start date: {}".format(config_dict['datei']),
            "End date: {}".format(config_dict['datef']),
            "Working directory: {}".format(config_dict['workdir']),
        ]
        
        map(lambda v: check.verbose(v), verbose_txt)
    
    @classmethod
    def load_setup(cls, plg,
                   parent_plg_type=None, level=None, **kwargs):
        """Loads a Setup plugin.
        Loops recursively over all attributes of the setup to load:
        1) sub-plugins are initialized as Plugin child-class templates (
        Domain, ObsVect, Model, etc);
        2) instances are saved to the Plugin class to be accessible for
        anywhere later one.
        
        This allows modifications of the data of a given plugin at some place
        of the code to be automatically forwarded to the rest of the code
        
        Args:
            self (Setup): the setup to load
            parent_plg_type (str): the last recognized plugin type that is
            inherited by children
        
        """
        
        # Update orig_dict if not yet defined
        if level == 0:
            # Saves level 0 entries as reference plugins in requirements
            cls._save_refplugins(plg)
        
        # Loop over self attributes and load them as other Class if necessary
        # If an argument 'todo_init' was specified, initialize only listed plg
        if 'todo_init' in cls._get_attribute_list(plg):
            attributes = plg.todo_init
        
        else:
            attributes = [a for a in cls._get_attribute_list(plg)
                          if a != 'plugin']

        # Keep in memory the root plg_type
        root_plg_type = parent_plg_type

        for attr in attributes:
            plg_attr = getattr(plg, attr)

            # Re-initializing parent type to the root
            parent_plg_type = root_plg_type

            # For reference instances, check whether the Plugin was already
            # initialized as requirement; if so, just take it from reference
            if attr in cls.reference_instances \
                    and getattr(plg_attr, 'isreference', False) \
                    and getattr(cls.reference_instances.get(attr, None),
                                'loaded_class', False):
                setattr(plg, attr, cls.reference_instances[attr])
                continue
            
            # If not a Plugin, continue
            if not issubclass(type(plg_attr), Plugin):
                continue
            
            # If is still a Setup class, means that should be processed and
            # Initialized
            if isinstance(plg_attr, Setup) \
                    and not getattr(plg_attr, 'loaded_class', False):
                # Load the plugin type depending on the attribute name
                # Do nothing if the attribute is named 'plugin'
                if attr != 'plugin':
                    parent_plg_type = \
                        plg_attr._load_plugin_type(attr,
                                                   parent_plg_type)

                # Build a child sub-class and
                # overwrite the Setup class if needed
                plg_attr = cls.childclass_factory(plg_attr,
                                                  child_type=parent_plg_type)
                
                # Keep in memory that the current attribute class is loaded
                plg_attr.loaded_class = True
            
            # Load all attributes recursively if not already done
            if not getattr(plg_attr, 'loaded_attributes', False):
                cls.load_setup(plg_attr, parent_plg_type,
                               **kwargs)
                plg_attr.loaded_attributes = True
            
            # Initializes the plugin from registered module if any
            if hasattr(plg_attr, 'initiate_template') \
                    and not getattr(plg_attr, 'loaded_template', False):
                plg_attr.initiate_template()

                # Saves the plugin to the class,
                # so it is accessible by everyone anywhere
                # (including its attributes and stored data)
                if hasattr(plg_attr, 'plugin'):
                    name = plg_attr.plugin.name
                    version = plg_attr.plugin.version
                    plg_type = plg_attr.plugin.type
                    
                    if not cls.is_loaded(name, version, plg_type) \
                            and name is not None:
                        cls.save_loaded(plg_attr)
                
                plg_attr.loaded_template = True
            
            # If requirements are not already loaded
            if not getattr(plg_attr, 'loaded_requirements', False):
                # Load requirements
                cls._check_requirements(plg_attr, **kwargs)
                
                # The plugin has been correctly loaded at this point
                plg_attr.loaded_requirements = True
            
            # Initializes the plugin data
            if hasattr(plg_attr, 'ini_data') \
                    and not getattr(plg_attr, 'loaded_data', False):
                plg_attr.ini_data(**kwargs)
                plg_attr.loaded_data = True
            
            # Linking present plugin to reference level 0 if needed
            if getattr(plg_attr, 'isreference', False):
                plg.reference_instances[attr] = plg_attr
            
            # Attach plugin to the parent plugin
            setattr(plg, attr, plg_attr)
    
    @classmethod
    def _check_requirements(cls, plg, **kwargs):
        """Checking that required modules and plugins are loaded.
        If not, load them.

        Requirements are defined in the __init__.py file of the
        corresponding plugin module.

        Args:
            plg (Plugin): a plugin to initialize

        Notes: Some basic parameters are added as requirements to all plugins;
        These are:
            'datei', 'datef', 'workdir', 'logfile', 'verbose'

        """
        
        # Dealing with default requirements supposed to be given at level 0
        for key in plg.default_requirements:
            if key not in cls._get_attribute_list(plg):
                if key in cls.reference_instances:
                    setattr(plg, key, cls.reference_instances[key])
                
                else:
                    raise PluginError("The default key '{}' is not prescribed"
                                      "neither in the plugin {}, nor in the "
                                      "level 0 of the configuration file"
                                      .format(key, plg))
        
        # Looping over requirements and including them
        for key in plg.requirements:
            key_req = plg.requirements[key]
            fromany = key_req.get('any', False)
            empty = key_req.get('empty')
            
            name = key_req.get('name', None)
            version = key_req.get('version', '')
            plg_type = key_req.get('type', key)
            newplg = key_req.get('newplg', False)
            
            # If not from any plugin, but no default value specified, error
            if not fromany and name is None:
                raise PluginError(
                    "{} needs a specifi {}, but none was specified \n"
                    "Please check requirements in your module"
                        .format(plg, key)
                )
            
            # If needs a Plugin explicitly defined,
            # look for it at level 0 of setup, or in children
            plg_out = None
            
            if fromany:
                # If in children
                if key in cls._get_attribute_list(plg):
                    plg_tmp = getattr(plg, key)
                    
                    # If child has a prescribed name
                    if getattr(getattr(plg_tmp, 'plugin', None), 'name', None) \
                            is not None:
                        plg_out = plg_tmp
                    
                    # If a default is defined, load from registered
                    elif name is not None:
                        plg_out = cls.load_registered(name, version, plg_type,
                                                      plg_orig=plg_tmp)
                    
                    # Otherwise, if accepts empty classes
                    elif empty:
                        plg_out = cls.get_subclass(plg_type)(plg_orig=plg_tmp)
                    
                    # Error in the yaml if reaching this point
                    else:
                        raise PluginError(
                            "{} needs a plugin '{}/{}/{}' and an "
                            "inconsistent one was proposed in the Yaml"
                                .format(plg, key, name, version)
                        )
                
                # If not in children but at level 0 of Yaml
                elif key in cls.reference_instances:
                    plg_tmp = cls.reference_instances[key]
                    
                    # If reference has a prescribed name
                    if getattr(getattr(plg_tmp, 'plugin', None), 'name', None) \
                            is not None:
                        plg_out = plg_tmp
                    
                    # If a default is defined, load from registered
                    elif name is not None:
                        plg_out = cls.load_registered(name, version, plg_type,
                                                      plg_orig=plg_tmp)
                    
                    # Otherwise, if accepts empty classes
                    elif empty:
                        plg_out = cls.get_subclass(plg_type)(plg_orig=plg_tmp)
                    
                    # Error in the yaml if reaching this point
                    else:
                        raise PluginError(
                            "{} needs a plugin '{}/{}/{}' and an "
                            "inconsistent one was proposed in the Yaml"
                                .format(plg, key, name, version)
                        )
                
                elif empty:
                    if cls.is_registered(name, version, plg_type):
                        plg_out = cls.load_registered(name, version, plg_type)
                    
                    else:
                        plg_out = cls.get_subclass(plg_type)()
            
            # If needs a specifi one
            else:
                # If in children
                if key in cls._get_attribute_list(plg):
                    plg_tmp = getattr(plg, key)
                    
                    # If child already of correct type, and correct ID
                    if plg_tmp.plugin.name is not None \
                            and name == plg_tmp.plugin.name \
                            and version == plg_tmp.plugin.version \
                            and type(plg_tmp) == cls.get_subclass(plg_type):
                        plg_out = plg_tmp
                    
                    # If a default is defined, load from registered
                    elif plg_tmp.plugin.name is None:
                        plg_out = cls.load_registered(name, version, plg_type,
                                                      plg_orig=plg_tmp)
                    
                    else:
                        raise PluginError(
                            "{} needs a specifi plugin '{}/{}/{}' and a "
                            "different was specified in children"
                                .format(plg, key, name, version)
                        )
                
                # If not in children but at level 0 of Yaml
                elif key in cls.reference_instances:
                    plg_tmp = cls.reference_instances[key]
                    
                    # If child already of correct type, and correct ID
                    if plg_tmp.plugin.name is not None \
                            and name == plg_tmp.plugin.name \
                            and version == plg_tmp.plugin.version \
                            and not newplg:
                        plg_out = plg_tmp
                    
                    # If a default is defined, load from registered
                    elif plg_tmp.plugin.name is None:
                        cls.reference_instances[key] = \
                            cls.load_registered(name, version, plg_type,
                                                plg_orig=plg_tmp)
                        plg_out = cls.reference_instances[key]
                    
                    else:
                        
                        raise PluginError(
                            "{} needs a specifi plugin '{}/{}/{}' and a "
                            "different was specified at level 0"
                                .format(plg, key, name, version)
                        )
                
                # If accepts empty class
                elif empty:
                    plg_out = cls.load_registered(name, version, plg_type)
            
            if plg_out is None:
                raise Exception(
                    "{} needs a Plugin '{}' to run properly\n"
                    "there is none in its children nor at the level 0 of "
                    "Yaml\n"
                    "Please check your Yaml"
                        .format(plg, key)
                )

            # Keep in memory to initialize a new instance of the plugin or not
            plg.plugin.newplg = newplg

            # Attaching the requirement to the parent plugin
            setattr(plg, key, plg_out)

        # Load the requirements if not already done
        cls.load_setup(plg, **kwargs)
