import numpy as np
import xarray as xr
import os
from pycif.utils.datastores.dump import dump_datastore, read_datastore
import scipy
from vinterp import vertical_interp


def native2obsvect(self, y0, datastore, ddi, ddf):
    """Aggregate simulations at the grid scale to total columns.
    Re-interpolate the model pressure levels to the satellite averaging kernel
    levels. Average using the averaging kernel formula

    """

    # Number of levels to extract for satellites
    dlev = np.ones(len(y0), dtype=int)
    dlev[y0['level'] < 0] = self.model.domain.nlev

    # Index in the original data of the level-extended dataframe
    native_inds = np.append([0], dlev.cumsum())[:-1]
    datastore['indorig'] = np.nan
    datastore.ix[native_inds, 'indorig'] = np.arange(len(y0))
    datastore['indorig'].fillna(method='ffill', inplace=True)
    datastore['indorig'] = datastore['indorig'].astype(int)

    # Building the extended dataframe
    iq1 = (np.abs(y0['level']) - np.abs((y0['level'] / 10.)
                                        .astype(int) * 10)) \
        .astype(int)
    nblinfo = ((y0['level'].astype(int) - y0['level']) * 1e7).astype(int)
    list_satIDs = iq1.loc[y0['level'] < 0].unique()

    ds_p = datastore.set_index('indorig')[['pressure', 'dp']]

    for satID in list_satIDs:
        satmask = iq1 == satID
        nobs = np.sum(satmask)

        nblloc = nblinfo.loc[satmask].values - 1

        # Stacking output datastore into levels * nobs
        native_ind_stack = native_inds[satmask] \
                    + np.arange(self.model.domain.nlev)[:, np.newaxis]

        # If all nans in datasim, meaning that the species was not simulated
        sim = datastore['sim'].values[native_ind_stack]
        if not np.any(~np.isnan(sim)):
            continue

        # Grouping all data from this satellite
        datasim = xr.Dataset(
            {'pressure': (['level', 'index'],
                          np.log(ds_p['pressure'].values[native_ind_stack])),
             'dp': (['level', 'index'], ds_p['dp'].values[native_ind_stack]),
             'sim': (['level', 'index'], sim)},
            coords={'index': nblloc,
                    'level': np.arange(self.model.domain.nlev)}
        )

        if 'sim_tl' in datastore:
            datasim['sim_tl'] = (['level', 'index'],
                                 datastore['sim_tl'].values[native_ind_stack])

        # Check whether there is some ak
        file_aks = ddi.strftime(
            '{}/obsvect/satellites/infos_{:02d}%Y%m%d%H%M.nc' \
                .format(self.workdir, satID))

        try:
            sat_aks = read_datastore(file_aks).to_xarray()

        except IOError:
            # Assumes total columns?
            # datastore['qdp'] = datastore['sim'] * datastore['dp']
            # groups = datastore.groupby(['indorig'])
            # y0.loc[:, 'sim'] += \
            #     groups['qdp'].sum().values / groups['dp'].sum().values
            #
            # if 'sim_tl' in datastore:
            #     datastore['qdp'] = datastore['sim_tl'] * datastore['dp']
            #     groups = datastore.groupby(['indorig'])
            #     y0.loc[:, 'sim_tl'] += \
            #         groups['qdp'].sum().values / groups['dp'].sum().values
            continue

        aks = sat_aks['ak'][nblloc, ::-1].T
        pavgs = 100. * sat_aks['pavg'][nblloc, ::-1].T
        pavgs = xr.DataArray(
            np.concatenate([pavgs, np.zeros((1, nobs))], axis=0),
            coords={'index': nblloc,
                    'level': np.arange(aks.level.size + 1)},
            dims=('level', 'index'))

        pavgs_mid = xr.DataArray(
            np.log(0.5 * (pavgs[:-1].values + pavgs[1:].values)),
            dims={'index': nblloc,
                  'level': np.arange(aks.level.size)})
        dpavgs = xr.DataArray(
            np.diff(- pavgs, axis=0),
            dims={'index': nblloc,
                  'level': np.arange(aks.level.size)})

        qa0lus = sat_aks['qa0lu'][nblloc, ::-1].T

        # Interpolating simulated values to averaging kernel pressures
        # Doing it by chunk to fasten the process
        # A single chunk overloads the memory,
        # while too many chunks do not take advantage
        # of scipy automatic parallelisation
        # 50 chunks seems to be fairly efficient
        sim_ak = 0. * pavgs_mid
        sim_ak_tl = 0. * pavgs_mid
        chunks = np.linspace(0, nobs, num=50, dtype=int)
        for k1, k2 in zip(chunks[:-1], chunks[1:]):
            print satID, k1, k2

            # Vertical interpolation
            xlow, xhigh, alphalow, alphahigh = \
                vertical_interp(datasim['pressure'][:, k1:k2].values,
                                pavgs_mid[:, k1:k2].values)

            # Applying coefficients
            meshout = np.array(pavgs_mid.shape[0] * [range(k2 - k1)])

            sim = datasim['sim'][:, k1:k2].values
            sim_ak[:, k1:k2] = alphalow * sim[xlow, meshout] \
                + alphahigh * sim[xhigh, meshout]

            if 'sim_tl' in datasim:
                sim_tl = datasim['sim_tl'][:, k1:k2].values
                sim_ak_tl[:, k1:k2] = alphalow * sim_tl[xlow, meshout] \
                    + alphahigh * sim_tl[xhigh, meshout]

        # # Correction with the pressure thickness
        # # WARNING: there is an inconsistency in the number of levels
        # sim_ak *= (datasim['dp'] * datasim['sim']).sum(axis=0).values \
        #           / (dpavgs * sim_ak).sum(axis=0).values \
        #           * dpavgs.sum(axis=0).values / datasim['dp'].sum(axis=0).values
        # if 'sim_tl' in datasim:
        #     sim_ak_tl *= \
        #         (datasim['dp'] * datasim['sim_tl']).sum(axis=0).values \
        #         / (dpavgs * sim_ak_tl).sum(axis=0).values \
        #         * dpavgs.sum(axis=0).values / datasim['dp'].sum(axis=0).values

        # Applying aks
        y0.loc[satmask, 'sim'] = \
            (sim_ak * dpavgs * aks.values).sum(axis=0) \
            / (dpavgs * aks.values).sum(axis=0)
        if 'sim_tl' in datasim:
            y0.loc[satmask, 'sim_tl'] = \
                (sim_ak_tl * dpavgs * aks.values).sum(axis=0) \
                / (dpavgs * aks.values).sum(axis=0)

    # Save forward datastore for later use by adjoint
    file_monit = ddi.strftime('{}/chain/monit_%Y%m%d%H%M.nc'
                             .format(self.model.adj_refdir))
    dump_datastore(datastore, file_monit=file_monit,
                   dump_default=False,
                   col2dump=['pressure', 'dp', 'indorig'],
                   mode='w')

    return y0
