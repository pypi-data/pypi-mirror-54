from fetch_meteo import fetch_meteo
from read_meteo import read_meteo

requirements = {'domain': {'name': 'LMDZ', 'version': 'std', 'empty': False}}


def ini_data(plugin, **kwargs):
    # Fetching meteo from pre-computed directory
    fetch_meteo(plugin,
                plugin.datei,
                plugin.datef,
                plugin.workdir)
    
    # Reads meteo to get info about time steps
    read_meteo(plugin,
               plugin.datei,
               plugin.datef,
               plugin.workdir)
