import datetime
import xarray as xr
import numpy as np
from pycif.utils.check import verbose
from pycif.utils.check.errclass import PluginError
from .utils.dates import dateslice
from utils.scalemaps import scale2map
from utils.reindex import reindex


def control2native(self, mod_input, di, df, mode,
                   runsubdir, workdir,
                   **kwargs):
    """Translates information in the control vector to real size-data. This
    is in preparation to the generation of proper model inputs from the
    real-size data
    
    Args:
        self (Plugin): the control vect to use to generate inputs
        mod_input (str): type of inputs to prepare
        di (datetime.datetime): starting date of the simulation window
        df (datetime.datetime): ending date of the simulation window
        mode (str): running mode: one of 'fwd', 'adj' and 'tl'
        runsubdir (str): sub-directory for the current simulation
        workdir (str): the directory of the whole pyCIF simulation
    
    Returns:
        xarray Dataset with native resolution control variables
    
    """
    # TODO: There is a hidden conceptual layer here
    # So far, it is assumed that inputs should have a direct corresponding
    # component in the control vector, whereas one would need a general
    # mapping function between the control vector structure and the inputs
    # structure
    # For instance, inversion setups can include only proxies of emissions
    # and not emissions directly; in that case, the control vector needs to
    # know how to translate the information between the two spaces

    ddi = min(di, df)
    ddf = min(di, df)

    # If this type of input is not considered in the control vector,
    # return nothing
    # It will then be handled as a fixed input
    if not hasattr(getattr(self, 'components', None), mod_input):
        verbose("Couldn't interpret {} in the control vector. "
                "Handling it as fixed input"
                .format(mod_input))
        return
    
    component = getattr(self.components, mod_input)
    xmod = {}
    for trcr in component.parameters.attributes:
        tracer = getattr(component.parameters, trcr)
        
        # Translates control vector, and increments if tangent-linear
        variables = {'scale': self.x}
        if mode == 'tl':
            variables['incr'] = self.dx
        
        # Deal with control vect dates and cut if controlvect period spans
        # outside the sub-simulation period
        dslice = dateslice(tracer, di, df)
        
        cdates = tracer.dates[dslice]
        if cdates[0] < ddi:
            cdates[0] = ddi

        # Translates only control variables corresponding to the
        # simulation period
        for x in variables:
            tmp = np.reshape(
                variables[x][tracer.xpointer:tracer.xpointer + tracer.dim],
                (tracer.ndates, tracer.nlev, -1))[dslice]

            # Deals with different resolutions
            variables[x] = scale2map(tmp, tracer, cdates,
                                     tracer.domain)
            
        xmod[trcr] = variables

        # Now deals with scalars and physical variables
        if getattr(tracer, 'type', 'scalar') == 'scalar':
            # Read the tracer array and apply the present control vector
            # scaling factor
            inputs = tracer.read(trcr, tracer.dir, tracer.file,
                                 self.model.input_dates[ddi],
                                 comp_type=mod_input,
                                 model=self.model,
                                 **kwargs)

            scale = reindex(xmod[trcr], 'scale',
                            levels={'time': inputs.time, 'lev': inputs.lev})
            xmod[trcr]['spec'] = inputs * scale

            if mode == 'tl':
                incr = reindex(xmod[trcr], 'incr',
                               levels={'time': inputs.time, 'lev': inputs.lev})
                xmod[trcr]['incr'] = incr * inputs

        # Data already contains the correct info for physical control variables
        # WARNING: so far, assumes that the vertical resolution is already
        # correct
        elif getattr(tracer, 'type', 'scalar') == 'physical':
            spec = reindex(xmod[trcr], 'scale',
                           levels={'time': self.model.input_dates[ddi],
                                   'lev': xmod[trcr]['scale'].lev})
            xmod[trcr]['spec'] = spec

            if mode == 'tl':
                incr = reindex(xmod[trcr], 'incr',
                           levels={'time': self.model.input_dates[ddi],
                                   'lev': xmod[trcr]['incr'].lev})
                xmod[trcr]['incr'] = incr

        # Removing the scaling factor as all information is stored in
        # 'spec' and 'incr' now
        xmod[trcr].pop('scale')

        # Saving reference directories if specified
        xmod[trcr]['fileorig'] = getattr(tracer, 'file', None)
        xmod[trcr]['dirorig'] = getattr(tracer, 'dir', None)

    return xmod
