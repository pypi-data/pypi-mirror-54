import shutil
from distutils.dir_util import copy_tree
from read_chemistry import read_chemicalscheme
from make_chemistry import create_chemicalscheme
from pycif.utils.check import verbose
from pycif.utils.path import init_dir


def ini_data(self, **kwargs):
    """Initializes the chemistry depending on the model used
    for the inversion.

    Args:
        plugin (ChemistryPlugin): chemistry definition

    Returns:
        Updates on the fly the chemistry
    """
    
    
    verbose('Initializing the Chemistry')
    
    # Copying the chemical scheme to the working directory
    workdir = self.workdir
    dirchem_ref = '{}/chemical_scheme/{}/'.format(workdir, self.schemeid)
    self.dirchem_ref = dirchem_ref
    
    shutil.rmtree(dirchem_ref, ignore_errors=True)
    init_dir(dirchem_ref)
    
    # If pre-computed scheme is specified
    if hasattr(self, 'dir_precomp'):
        copy_tree('{}/{}/'.format(self.dir_precomp, self.schemeid),
                  dirchem_ref)
    
        # Read chemistry
        self.read_chemicalscheme(**kwargs)
    
    # Otherwise, initialize files from the yaml
    else:
        self.create_chemicalscheme()
