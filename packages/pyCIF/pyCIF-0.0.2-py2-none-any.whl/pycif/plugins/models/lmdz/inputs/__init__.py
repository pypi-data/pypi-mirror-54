import os
import shutil

from params import make_rundef, make_totinput
from pycif.utils import path
from pycif.utils.check import verbose


def make_input(self, mod_input, di, df, mode, runsubdir, workdir,
               lmdz_yearref=1979, **kwargs):
    """Prepares inputs for the current LMDZ simulation. It includes:
        - meteo files (defstoke.nc, fluxstoke.nc fluxstokev.nc and phystoke.nc)
        - def files (run.def, totinput, ACTIVE_SPECIES)
        - initial conditions (start.nc)
        - fields for SACS (inca.nc, incaMCF.nc)

    Args:
        - self (Plugin): LMDZ plugin
        - mod_input (str): one of: 'meteo', 'def', 'inicond', 'chem_fields'
        - di (datetime): beginning of the simulation window (along the fwd
        or bckwd axis)
        - df (datetime): end of simulation
        - workdir (str): path to the pycif simulation
        - runsubdir (str): path to the LMDZ sub-simulation
        - mode (str): running mode; fwd or adj
        - lmdz_yearref (int): reference year for LMDZ dates. Default is 1979

    """

    datei = min(di, df)
    
    if mod_input == 'meteo':
        # Links meteorological mass fluxes
        for ftype in ['defstoke', 'fluxstoke', 'fluxstokev', 'phystoke']:
            meteo_file = "{}.an{}.m{:02d}.nc".format(ftype,
                                              datei.year, datei.month)
            
            source = '{}/meteo/{}'.format(workdir, meteo_file)
            target = '{}/{}.nc'.format(runsubdir, ftype)
            
            if ftype == 'defstoke' and not os.path.isfile(source):
                meteo_file = "{}.nc".format(ftype)
                source = '{}/meteo/{}'.format(workdir, meteo_file)
            
            path.link(source, target)
        
        # Links vertical coordinates from previous simulations
        source = self.file_vcoord
        target = '{}/vcoord.nc'.format(runsubdir)
        path.link(source, target)
        
    elif mod_input == 'def':
        # run.def
        make_rundef(self.filedef, datei, self.physic, runsubdir, lmdz_yearref)
        
        # totinput
        make_totinput(self, runsubdir, datei, mode)
        
        # Remove restart TL
        if mode != 'tl':
            shutil.rmtree('{}/*start_tl.bin'.format(runsubdir),
                          ignore_errors=True)
        
        # TODO: at the moment, no satellite observation
        os.system('echo 0 > {}/infousedsat.txt'.format(runsubdir))
        
    elif mod_input == 'chem_fields':
        if hasattr(self, 'chemistry'):
            # Linking to pre-computed INCA fields for kinetics
            source = \
                datei.strftime("{}/{}".format(
                    self.chemistry.kinetic.dir,
                    self.chemistry.kinetic.file))
            target = "{}/kinetic.nc".format(runsubdir)
            path.link(source, target)
            
            # Linking to pre-computed INCA fields for deposition
            if hasattr(self.chemistry, 'deposition'):
                for spec in self.chemistry.deposition.attributes:
                    tracer = getattr(self.chemistry.deposition, spec)
                    source = \
                        datei.strftime("{}/{}".format(
                            tracer.dir, tracer.file))
                    target = "{}/dep_{}.nc".format(runsubdir, spec)
                    path.link(source, target)

            finf = '{}/chemical_scheme.nml'.format(self.chemistry.dirchem_ref)
            target = '{}/chemical_scheme.nml'.format(runsubdir)
            path.link(finf, target)
            
    elif mod_input == 'traj':
        if mode == 'adj':
            if not hasattr(self, 'adj_refdir'):
                verbose("Adjoint LMDZ couldn't be initialized "
                        "with forward trajq.bin files")
                raise Exception
            
            else:
                for spec in self.chemistry.acspecies.attributes:
                    traj_file = "trajq_{}_%Y%m%d%H%M.bin".format(spec)
                    source = datei.strftime(
                        "{}/chain/{}".format(
                            self.adj_refdir, traj_file))
                    target = "{}/trajq_{}.bin".format(runsubdir, spec)
                    
                    path.link(source, target)
                

