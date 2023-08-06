from pycif.utils import path


def make_meteo(self, runsubdir, sdc):
    print "Deals with meteo"
    # use ready-made METEO.nc files
    # Getting the right one
    nho=self.nho
    filemet = self.meteo.dir+ \
        'METEO.' + sdc + '.' + str(nho) + '.nc'
    path.link(filemet, runsubdir + '/METEO.nc')
