import numpy as np
import string
import pycif.utils.check as check
from pycif.utils.path import init_dir
import pandas as pd
import os


def read_chemicalscheme(chemistry,
                        **kwargs):
    """Reads a chemical scheme from existing files

    Args:
        chemistry (pycif.utils.classes.chemistries.Chemistry): the chemical
            scheme

    Return:
        Grid dictionary with characteristics of the chemical scheme

    Notes:

    """
    
    check.verbose('Reading Chemistry')
    
    workdir = chemistry.workdir
    dirchem_ref = '{}/chemical_scheme/{}/'.format(workdir, chemistry.schemeid)
    
    # ACTIVE SPECIES
    file_chem = '{}/ACTIVE_SPECIES.{}'.format(dirchem_ref,
                                             chemistry.schemeid)
    chemistry.species = pd.read_csv(file_chem, header=None, sep=' ',
                                    usecols=[0, 1], names=['ID', 'name'])
    chemistry.nspec = len(chemistry.species)
    
    # ANTHROPIC
    file_chem = '{}/ANTHROPIC.{}'.format(dirchem_ref,
                                        chemistry.schemeid)
    chemistry.anthro_species = pd.read_csv(file_chem, header=None, sep=' ',
                                    usecols=[0, 1], names=['ID', 'name'])
    chemistry.nemisa = len(chemistry.anthro_species)
    
    # BIOGENIC
    file_chem = '{}/BIOGENIC.{}'.format(dirchem_ref,
                                       chemistry.schemeid)
    chemistry.bio_species = pd.read_csv(file_chem, header=None, sep=' ',
                                    usecols=[0, 1], names=['ID', 'name'])
    chemistry.nemisb = len(chemistry.bio_species)
    
    # DEPO_SPEC
    file_chem = '{}/DEPO_SPEC.{}'.format(dirchem_ref,
                                        chemistry.schemeid)
    chemistry.dep_species = pd.read_csv(file_chem, header=None, sep=' ',
                                    usecols=[0, 1], names=['ID', 'name'])
    chemistry.ndep = len(chemistry.dep_species)
    
    # CHEMISTRY
    with open(dirchem_ref + 'CHEMISTRY.' + chemistry.schemeid, 'r') as fsp:
        ln = fsp.readlines()
        chemistry.nreac = len(ln)
    
    with open(dirchem_ref + 'FAMILIES.' + chemistry.schemeid, 'r') as fsp:
        ln = fsp.readlines()
        chemistry.nfam = len(ln)
    
    chemistry.nspresc = 4  ##### en dur pour le moment
