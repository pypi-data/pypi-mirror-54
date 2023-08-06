#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import xarray as xr


def make_fluxes(self, datastore, ddi, ddf, runsubdir, mode):
    """

    :param self:
    :param datastore:
    :param ddi:
    :param ddf:
    :return:
    """

    for spec in self.emis_species.attributes:
        # If determined by the control vector
        if spec in datastore:
            data = datastore[spec]

        # Else read directly from netCDF files
        else:
            tracer = getattr(self.emis_species, spec)

            data = {'spec': self.emis_species.read(
                spec, tracer.dir, tracer.file, self.input_dates[ddi])}

        # Adds empty increments if not available
        if 'incr' not in data:
            data['incr'] = 0. * data['spec']

        # Put in dataset for writing by 'write'
        ds = xr.Dataset({'fwd': data['spec'],
                         'tl': data['incr']})

        # Write to FORTRAN binary
        flx_file = "{}/mod_{}.bin".format(runsubdir, spec)
        self.fluxes.write(flx_file, ds)
