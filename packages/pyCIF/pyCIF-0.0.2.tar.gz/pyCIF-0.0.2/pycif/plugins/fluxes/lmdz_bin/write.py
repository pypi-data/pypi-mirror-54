from scipy.io import FortranFile
import numpy as np
from pycif.utils.classes.fluxes import Fluxes
import xarray


def write(self, flx_file, flx):
    """Write flux to LMDZ-DISPERSION compatible files.
    The shape follows the LMDZ physical vectorial shape grid.
    Each line of the output binary file includes.
    
    Args:
        self (Fluxes): the Fluxes plugin
        file (str): the file where to write fluxes
        flx (xarray.Dataset): fluxes data to write
        """

    with FortranFile(flx_file, 'w') as f:
        # Looping over all values and writing to binary
        flx_fwd = flx['fwd'].values
        flx_tl = flx['tl'].values
        for f0, f1 in zip(np.ravel(flx_fwd), np.ravel(flx_tl)):
            f.write_record(np.array([f0, f1], dtype=float))
