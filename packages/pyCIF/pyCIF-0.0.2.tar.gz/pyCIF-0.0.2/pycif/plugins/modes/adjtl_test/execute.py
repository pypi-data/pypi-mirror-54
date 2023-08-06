import numpy as np
import copy
from pycif.utils.check import verbose


def execute(self, **kwargs):
    """Runs the model in forward mode

    Args:
        self (Plugin): the mode Plugin with all set-up arguments

    """
    
    # Working directory
    workdir = self.workdir
    
    # Control vector
    controlvect = self.controlvect

    # Observation operator
    obsoper = self.obsoperator
    
    # Simulation window
    datei = self.datei
    datef = self.datef




    # Increments in x
    increments = getattr(self, 'increments', 0.)
    incrmode = getattr(self, 'incrmode', 'cst')
    testspace = getattr(self, 'testspace', 'control')
    
    if testspace == 'control':
        if incrmode == 'cst':
            controlvect.dx = increments * controlvect.std
        
        elif incrmode == 'rand':
            controlvect.dx = np.random.normal(0, increments, controlvect.dim) \
                             * controlvect.std
    
    elif testspace == 'chi':
        if incrmode == 'cst':
            controlvect.chi[:] = increments
        
        elif incrmode == 'rand':
            controlvect.chi = \
                np.random.normal(0, increments, controlvect.chi_dim)
        
        controlvect.dx = \
            controlvect.sqrtbprod(controlvect.chi, **kwargs) - controlvect.xb
    
    if testspace not in ['control', 'chi'] \
            or incrmode not in ['cst', 'rand']:
        verbose("The increment mode you specified can't be parsed: {}"
                .format(incrmode))
        verbose("Please check the definition of the running mode "
                "in your Yaml file")
        raise Exception
    
    controlvect.x = copy.deepcopy(controlvect.xb)
    controlvect.xb += controlvect.dx

    # Some verbose
    verbose("Computing the test of the adjoint")
    
    # Get the machine accuracy
    accuracy = np.finfo(np.float64).eps

    # Running the tangent linear code of the model
    obsvect = obsoper.obsoper(controlvect, 'tl',
                              datei=datei, datef=datef,
                              workdir=workdir,
                              reload_results=getattr(self, 'reload_results',
                                                     False),
                              **kwargs)

    # Computing < H.dx, H.dx >
    scaleprod1 = obsvect.datastore['sim_tl'].pow(2.).sum()

    # Putting increments in the observation vector
    obsvect.datastore['obs_incr'] = obsvect.datastore['sim_tl']
    obsvect.datastore.loc[
        np.isnan(obsvect.datastore['obs_incr']), 'obs_incr'] = 0

    # Running the observation operator
    controlvect = obsoper.obsoper(obsvect, 'adj',
                                  datei=datei, datef=datef,
                                  workdir=workdir,
                                  reload_results=getattr(self, 'reload_results',
                                                         False),
                                  **kwargs)
    
    # Computing < dx, H*(H.dx) >
    if testspace == 'control':
        scaleprod2 = ((controlvect.xb - controlvect.x)
                      * controlvect.dx).sum()

    elif testspace == 'chi':
        scaleprod2 = \
            (controlvect.sqrtbprod_ad(controlvect.dx, **kwargs) *
             controlvect.chi).sum()

    else:
        scaleprod2 = np.nan

    # Final verbose
    verbose('Machine accuracy: {}'.format(accuracy))
    verbose('< H.dx, H.dx >   = {:.17E}'.format(scaleprod1))
    verbose('< dx, H*(H.dx) > = {:.17E}'.format(scaleprod2))
    verbose('The difference is {:.1E} times the machine accuracy'
            .format(np.abs(scaleprod2 / scaleprod1 - 1) / accuracy))
    