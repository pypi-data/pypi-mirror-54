import pandas as pd
import numpy as np


def obsvect2native(self, y0, mode, ddi, ddf):
    # Increments are scaled according to dtstep in the adjoint
    # This assumes that obs values are averages from sub-step values
    # TODO: more complex operations might be considered in the future:
    # e.g., interpolation, gradients, etc.
    # These should anyway be dealt with
    # at the obsvect level and not here
    if mode == 'adj':
        y0.loc[:, 'obs_incr'] /= y0['dtstep']

    # Observations overlapping two simulation sub-periods are dealt with
    model = self.model

    subsimu_dates = model.subsimu_dates
    tstep_dates = model.tstep_dates
    tstep_all = model.tstep_all

    # Cropping observations starting before the sub-simulation
    mask = (y0.index < ddi)
    y0.loc[mask, 'tstep'] = 0
    y0.loc[mask, 'dtstep'] -= np.argmax(tstep_all == ddi) \
                              - y0.loc[mask, 'tstep_glo']

    # Cropping observations starting before the sub-simulation
    if y0.size > 0:
        mask = (y0.index + pd.to_timedelta(y0['duration'], unit='h') > ddf)
        y0.loc[mask, 'dtstep'] = np.argmax(tstep_all == ddf) \
                                 - y0.loc[mask, 'tstep_glo']

        # For observations from several sub-periods back in time,
        # cropping to the full sub-period extend
        y0.loc[mask, 'dtstep'] = np.minimum(y0.loc[mask, 'dtstep'],
                                            len(tstep_dates[ddi]) - 1)

    # Change type to integer
    y0.loc[~np.isnan(y0['tstep']), 'tstep'] = \
        y0['tstep'][~np.isnan(y0['tstep'])].astype(int)
    y0.loc[~np.isnan(y0['dtstep']), 'dtstep'] = \
        y0['dtstep'][~np.isnan(y0['dtstep'])].astype(int)

    return y0


def native2obsvect(self, y0, mask):

    y0.loc[:, 'sim'] /= self.datastore.loc[mask, 'dtstep']

    if 'sim_tl' in y0:
        y0.loc[:, 'sim_tl'] /= self.datastore.loc[mask, 'dtstep']

    return y0

