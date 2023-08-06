from fetch_meteo import fetch_meteo
from read_meteo import read_meteo
from create_meteo import create_meteo

requirements = {'domain': {'name': 'dummy', 'version': 'std', 'empty': False}}


def ini_data(plugin, **kwargs):
    # Fetching meteo from pre-computed directory
    fetch_meteo(plugin,
                plugin.datei,
                plugin.datef,
                plugin.workdir)
