import numpy as np
import pickle

import pycif.utils.check as check


def execute(self, **kwargs):
    """Performs a variational inversion given a minimizer method and a
    simulator (i.e. a function to minimize and its gradient)

    Args:
        self (Plugin): definition of the mode set-up

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
    
    # Minimizer
    minimizer = self.minimizer
    
    # Simulator
    simulator = self.simulator
    
    # Some verbose
    towrite = \
        """
        Running a variational inversion with the following modules:
            Minimizer: {}
            Simulator: {}
        """.format(minimizer.plugin.name,
                   simulator.plugin.name)
    check.verbose(towrite)
    
    # Initial run of the simulator as a starting point for M1QN3
    costinit, gradinit = \
        simulator.simul(controlvect.chi,
                        run_id=-1,
                        **kwargs)
    
    zgnorm = np.sqrt(np.sum(gradinit ** 2))
    check.verbose('Nb of observations: ' + str(len(obsoper.obsvect.datastore)))
    check.verbose('Initial cost: ' + str(costinit))
    check.verbose('Initial gradient norm: ' + str(zgnorm))
    
    # Runs the minimizer
    chiopt = \
        minimizer.minimize(
            costinit, gradinit, controlvect.chi,
            **kwargs)
    
    # Last call to the simulator for final diagnostics
    costend, gradend = \
        simulator.simul(chiopt,
                        run_id=-2,
                        **kwargs)
    
    zgnorm = np.sqrt(np.dot(gradend, gradend)) / zgnorm
    check.verbose('Final cost: ' + str(costend))
    check.verbose('Ratio final/initial gradient norm: ' + str(zgnorm))
    
    # Save results
    controlvect.dump(
        '{}/controlvect_final.pickle'.format(workdir),
        to_netcdf=getattr(self, 'save_out_netcdf', False),
        dir_netcdf='{}/controlvect/'.format(workdir))
    
    return chiopt
