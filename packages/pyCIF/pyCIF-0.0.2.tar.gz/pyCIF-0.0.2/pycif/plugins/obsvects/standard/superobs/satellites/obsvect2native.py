import numpy as np
import pandas as pd
import os
import xarray as xr
from pycif.utils.datastores.dump import dump_datastore, read_datastore
import scipy
from vinterp import vertical_interp


def obsvect2native(self, y0, mode, ddi, ddf):
    """De-aggregate total columns to the model level."""

    # Number of levels to extract for satellites
    dlev = np.ones(len(y0), dtype=int)
    dlev[y0['level'] < 0] = self.model.domain.nlev

    # Index in the original data of the level-extended dataframe
    native_inds = np.append([0], dlev.cumsum())

    # Output index
    idx = np.zeros((native_inds[-1]), dtype=int)
    idx[native_inds[:-1]] = np.arange(len(y0))
    np.maximum.accumulate(idx, out=idx)
    native_inds = native_inds[:-1]

    # Output dataframe
    datacol = 'obs_incr' if mode == 'adj' else 'obs'
    col2process = ['tstep', 'i', 'j', 'level', 'dtstep', 'parameter',
                   datacol]
    df = y0.ix[idx, col2process]

    # Levels
    sublevels = \
        np.meshgrid(range(self.model.domain.nlev),
                    np.ones(np.where(y0['level'] <= 0)[0].size))[0].flatten()
    df.loc[df['level'] <= 0, 'level'] = sublevels

    # Stop here if not adjoint
    if mode != 'adj':
        return df

    # Load pressure coordinates from previous run
    file_monit = ddi.strftime('{}/chain/monit_%Y%m%d%H%M.nc'
                             .format(self.model.adj_refdir))
    fwd_pressure = read_datastore(file_monit).set_index('indorig')

    # Building the extended dataframe
    iq1 = (np.abs(y0['level']) - np.abs((y0['level'] / 10.)
                                        .astype(int) * 10)) \
        .astype(int)
    nblinfo = ((y0['level'].astype(int) - y0['level']) * 1e7).astype(int)
    list_satIDs = iq1.loc[y0['level'] < 0].unique()

    for satID in list_satIDs:
        satmask = iq1 == satID
        nobs = np.sum(satmask)

        nblloc = nblinfo.loc[satmask].values - 1

        # Getting the vector of increments
        obs_incr = y0.loc[satmask, 'obs_incr']

        # If all increments are NaNs, just pass to next satellite
        if not np.any(obs_incr != 0.):
            continue

        # Get target pressure
        native_ind_stack = native_inds[satmask] \
                    + np.arange(self.model.domain.nlev)[:, np.newaxis]
        datasim = xr.Dataset(
            {'pressure':
                 (['level', 'index'],
                  np.log(fwd_pressure['pressure'].values[native_ind_stack])),
             'dp': (['level', 'index'],
                    fwd_pressure['dp'].values[native_ind_stack])},
            coords={'index': nblloc,
                    'level': np.arange(self.model.domain.nlev)})

        # Getting averaging kernels
        file_aks = ddi.strftime(
            '{}/obsvect/satellites/infos_{:02d}%Y%m%d%H%M.nc' \
                .format(self.workdir, satID))

        try:
            sat_aks = read_datastore(file_aks).to_xarray()

        except IOError:
            # Assumes total columns?
            # groups = fwd_pressure.groupby(['indorig'])
            # df['obs_incr'] = y0.ix[idx, 'obs_incr'] * fwd_pressure['dp'] \
            #                  / groups['dp'].sum().values[idx]
            continue

        # Defining ak info
        aks = sat_aks['ak'][nblloc, ::-1].T
        pavgs = 100. * sat_aks['pavg'][nblloc, ::-1].T
        pavgs = xr.DataArray(
            np.concatenate([pavgs, np.zeros((1, nobs))], axis=0),
            coords={'index': nblloc,
                    'level': np.arange(aks.level.size + 1)},
            dims=('level', 'index'))
        pavgs_mid = xr.DataArray(
            np.log(0.5 * (pavgs[:-1].values + pavgs[1:].values)),
            coords={'index': nblloc,
                    'level': np.arange(aks.level.size)},
            dims=('level', 'index'))
        dpavgs = xr.DataArray(
            np.diff(- pavgs, axis=0),
            coords={'index': nblloc,
                    'level': np.arange(aks.level.size)},
            dims=('level', 'index'))

        # Applying aks
        obs_incr = dpavgs * aks.values / (dpavgs * aks.values).sum(axis=0) \
                   * obs_incr.values

        # Adjoint of the log-pressure interpolation
        obs_incr_interp = 0. * datasim['pressure'].values

        nchunks = getattr(self, 'nchunks', 50)
        chunks = np.linspace(0, nobs, num=nchunks, dtype=int)
        for k1, k2 in zip(chunks[:-1], chunks[1:]):
            # Vertical interpolation
            xlow, xhigh, alphalow, alphahigh = \
                vertical_interp(datasim['pressure'][:, k1:k2].values,
                                pavgs_mid[:, k1:k2].values)

            # Applying coefficients
            # WARNING: There might be repeated indexes in a given column
            # To deal with repeated index, np.add.at is recommended
            levmeshout = np.array((k2 - k1)
                                  * [range(pavgs_mid.shape[0])]).T
            meshout = np.array(pavgs_mid.shape[0] * [range(k1, k2)])

            np.add.at(obs_incr_interp, (xlow, meshout),
                      obs_incr.values[levmeshout, meshout] * alphalow)

            np.add.at(obs_incr_interp, (xhigh, meshout),
                      obs_incr.values[levmeshout, meshout] * alphahigh)

        # # Correction with the pressure thickness
        # obs_incr_interp *=\
        #     (dpres * obs_incr_interp).sum(axis=0) \
        #     / (dpavgs * obs_incr).sum(axis=0) \
        #     * dpavgs.sum(axis=0) / dpres.sum(axis=0)

        # Applying increments to the flattened datastore
        df.ix[native_ind_stack.flatten(), 'obs_incr'] = \
            obs_incr_interp.flatten()

    return df

