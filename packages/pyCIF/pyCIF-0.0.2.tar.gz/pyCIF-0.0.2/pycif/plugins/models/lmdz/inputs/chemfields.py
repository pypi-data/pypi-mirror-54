import numpy as np
from scipy.io import FortranFile
from pycif.utils import path
import pandas as pd


def make_chemfields(self, datastore, input_type, ddi, ddf, runsubdir, mode):
    # Deals only with species whose prodloss is activated
    if not hasattr(getattr(self, 'chemistry', None), input_type):
        return

    # Binary and nc file name depending on input_type
    bin_name = 'prodscale' if input_type == 'prodloss3d' else 'scale'
    nc_name = 'prodloss' if input_type == 'prodloss3d' else 'prescr'

    for spec in getattr(self.chemistry, input_type).attributes:
        if spec in datastore:
            data = datastore[spec]

            # Re-samples at daily scale
            day_dates = pd.date_range(ddi, ddf, freq='D').union([ddf])

            prod = data['scale'].to_dataframe(name='scale') \
                .unstack(level=['lat', 'lon']) \
                .reindex(day_dates, method='ffill') \
                .stack(level=['lat', 'lon']).to_xarray()['scale'] \
                .rename({'level_0': 'time'})

            # Keeping only data in the simulation window
            mask = (prod.time >= np.datetime64(ddi, 'ns')) \
                   & (prod.time <= np.datetime64(ddf, 'ns'))
            mask = np.where(mask)[0]

            prod = prod[mask]

            # If tangent-linear mode, include tl increments
            if 'incr' in data and mode == 'tl':
                incr = data['incr'].to_dataframe(name='incr') \
                           .unstack(level=['lat', 'lon']) \
                           .reindex(day_dates, method='ffill') \
                           .stack(level=['lat', 'lon']) \
                           .to_xarray()['incr'] \
                           .rename({'level_0': 'time'})[mask, :, :]
            else:
                incr = 0. * prod

            # Write to FORTRAN binary
            prod_file = "{}/mod_{}_{}.bin".format(runsubdir, bin_name, spec)
            with FortranFile(prod_file, 'w') as f:
                # Looping over all values and writing to binary
                prod = prod.values
                incr = incr.values
                for d0, d1 in zip(np.ravel(prod), np.ravel(incr)):
                    f.write_record(np.array([d0, d1], dtype=float))

        # Links reference netCDF files that are needed anyway by LMDZ
        try:
            dirorig = datastore[spec]['dirorig']
            fileorig = datastore[spec]['fileorig']

            if fileorig is None or dirorig is None:
                raise KeyError

        except KeyError:
            tracer = getattr(getattr(self.chemistry, input_type), spec)

            dirorig = tracer.dir
            fileorig = tracer.file

        origin = \
            ddi.strftime("{}/{}".format(dirorig, fileorig))

        target = "{}/{}_{}.nc".format(runsubdir, nc_name, spec)
        path.link(origin, target)