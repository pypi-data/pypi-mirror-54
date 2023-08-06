from pycif.utils.check import verbose
from pycif.utils.datastores.dump import dump_datastore
import numpy as np


def execute(self, **kwargs):
    """Runs the model in forward mode

    Args:
        setup (Plugin): definition of the full set-up

    """
    
    # Working directory
    workdir = self.workdir
    
    # Control vector
    controlvect = self.controlvect
    
    # Observation operator
    obsoper = self.obsoperator
    
    # Simulation window
    datei = self.datei
    datef = self.datef
    
    # Some verbose
    verbose("Running a direct run")
    
    # Putting x at xb value if available
    if hasattr(controlvect, 'xb'):
        controlvect.x = controlvect.xb
    
    # Running the observation operator
    obsvect = obsoper.obsoper(controlvect, 'fwd',
                              datei=datei, datef=datef,
                              workdir=workdir,
                              **kwargs)
    
    # Perturbs the output monitor if required in the Yaml
    if getattr(self, 'perturb_obsvect', False):
        # Altering obsvect and save data
        obserror = self.obserror * obsvect.datastore['sim'].mean()
        
        obsvect.datastore['obs'] = \
            np.random.normal(loc=0, scale=obserror,
                             size=obsvect.datastore.index.size) \
            + obsvect.datastore['sim']
        obsvect.datastore['obserror'] = obserror
        
        # Dumping the datastore with reference data
        dump_datastore(obsvect.datastore,
                       file_monit=obsvect.file_obsvect,
                       dump_type='nc', mode='w')

        print obsvect.file_obsvect
    
    return obsvect

