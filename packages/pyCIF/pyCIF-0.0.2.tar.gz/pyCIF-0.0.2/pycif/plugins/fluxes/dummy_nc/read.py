import pandas as pd
import pycif.utils.check as check
from pycif.utils import path
import xarray as xr
import datetime
import numpy as np


def read(self, name, tracdir, tracfile, dates,
                interpol_flx=False, **kwargs):
    """Get fluxes from pre-computed fluxes and load them into a pycif
    variables

    Args:
        self: the model Plugin
        name: the name of the component
        tracdir, tracfile: flux directory and file format
        dates: list of dates to extract
        interpol_flx (bool): if True, interpolates fluxes at time t from
        values of surrounding available files

    """
    
    check.verbose("READING NetCDF dummy fluxes")
    
    raise Exception
