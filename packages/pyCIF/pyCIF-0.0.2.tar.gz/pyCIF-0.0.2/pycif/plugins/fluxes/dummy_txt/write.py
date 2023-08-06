import numpy as np


def write(self, flx_file, flx_fwd, flx_tl):
    """Write fluxes for the dummy_txt Gaussian model.

    Args:
        self (Fluxes): the Fluxes plugin
        file (str): the file where to write fluxes
        flx_fwd, flx_tl: fluxes data to write
        """
    
    np.savetxt('{}.tl'.format(flx_file), flx_tl, delimiter=',')
    np.savetxt('{}.fwd'.format(flx_file), flx_fwd, delimiter=',')
