import pandas as pd
import datetime

from pycif.utils.check import verbose


def crop_monitor(datastore, datei, datef, **kwargs):
    """Crops observation datasets to keep observations whose duration fits
    entirely during the simulation period
    
    Args:
        datastore (pd.DataFrame): observation dataset
        datei (datetime.datetime): start date
        datef (datetime.datetime): end date
    
    Returns:
        pd.DataFrame: Cropped dataframe
    """
    
    verbose("Cropping obsvect.datastore to simulation window")
    verbose("{} to {}".format(datei, datef))
    
    mask = (datastore.index >= datei) \
           & (datastore.index
              + pd.to_timedelta(datastore['duration'], unit='h') <= datef)
    return datastore.loc[mask]
