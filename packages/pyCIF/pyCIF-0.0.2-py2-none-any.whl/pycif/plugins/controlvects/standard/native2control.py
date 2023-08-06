import datetime
import numpy as np

from pycif.utils.check import verbose
from .utils.dates import dateslice
from .utils.scalemaps import map2scale, vmap2vaggreg


def native2control(self, datastore, di, df,
                   workdir, runsubdir,
                   **kwargs):
    """Translates real-size data as extracted from the model outputs to
    the control space. This includes mainly temporal and spatial aggregation.
    This routine is used in adjoint mode, thus computes operations on
    increments.

    Args:
        self (Plugin): the control vect
        datastore (dict): the data at the model resolution to be converted
                          to the control space
        di (datetime): starting date of the simulation window
        df (datetime): ending date of the simulation window
        workdir (str): pycif working directory
        
    """
    
    # Check that the model provides information about sensitivities
    if 'adj_out' not in datastore:
        verbose("Couldn't get any model sensitivity. Assuming zero sensitivity")
        self.dx = 0. * self.x
        return
    
    # If dx is not yet defined, initialize it
    if not hasattr(self, 'dx'):
        verbose("Setting dx to zero in the control vector")
        self.dx = 0. * self.x
    
    # Loop over model sensitivities
    for mod_input in datastore['adj_out']:
        # If this type of input is not considered in the control vector,
        # ignoring the model sensitivity
        if not hasattr(getattr(self, 'components', None), mod_input):
            verbose("{} is sensitive to {} but your control vector doesn't "
                    "include it as a component"
                    .format(self.model.plugin.name, mod_input))
            continue
        
        component = getattr(self.components, mod_input)
        for trcr in datastore['adj_out'][mod_input]:
            # Skip tracers not in the control space
            if not hasattr(component.parameters, trcr):
                verbose("{} is sensitive to {} as a {} "
                        "but your control vector doesn't "
                        "include it as a component"
                        .format(self.model.plugin.name, trcr, mod_input))
                continue
            
            # Ignore initial conditions if not the first sub-period
            if mod_input == 'inicond' and self.datei != min(di, df):
                verbose("Initial conditions for {} are not considered "
                        "for sub-period {} compared to general start date {}"
                        .format(trcr, min(di, df), self.datei))
                continue
            
            # Process other input types:
            # - re-project map sensitivities to control space
            # - sum date slices in the sensitivities to control space periods
            tracer = getattr(component.parameters, trcr)
            
            dslice = dateslice(tracer, di, df)
            
            # For variables stored as a scaling factor,
            # scaling by the original value
            phys = np.ones((len(dslice)))
            if getattr(tracer, 'type', 'scalar') == 'scalar':
                phys = \
                    tracer.read(
                        trcr, tracer.dir, tracer.file, tracer.dates[dslice],
                        comp_type=mod_input, model=self.model,**kwargs).data

            # Loop over control space periods for temporal aggregation
            # Make vertical aggregation per temporal slice
            data = datastore['adj_out'][mod_input][trcr]['data']
            data_dates = datastore['adj_out'][mod_input][trcr]['dates']
            for idd, ds in enumerate(dslice):
                dd0 = tracer.dates[ds]
                dd1 = tracer.dates[min(ds + 1, tracer.ndates - 1)]
                
                # Either take the corresponding slice of time,
                # or take the exact date
                # if the control variable is on a time stamp
                if dd0 < dd1:
                    mask = (data_dates >= dd0) & (data_dates < dd1)
                else:
                    mask = data_dates == dd0

                # Vertical aggregation
                vdata = np.sum(data[mask], axis=0) * phys[idd]
                vaggreg = vmap2vaggreg(vdata[np.newaxis], tracer, tracer.domain)

                # 2d maps to control vector slices
                self.dx[tracer.xpointer:tracer.xpointer + tracer.dim][
                        ds * tracer.hresoldim * tracer.vresoldim:
                        (ds + 1) * tracer.hresoldim * tracer.vresoldim] += \
                    map2scale(vaggreg, tracer, tracer.domain).flatten()
                
                
