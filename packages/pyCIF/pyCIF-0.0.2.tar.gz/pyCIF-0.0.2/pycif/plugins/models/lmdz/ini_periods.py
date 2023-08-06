from pycif.utils.dates import date_range


def ini_periods(self, **kwargs):
    datei = self.datei
    datef = self.datef
    
    # List of sub-simulation windows
    self.subsimu_dates = \
        date_range(datei, datef, period=self.periods)
    
    # Dynamical and physical time step for LMDZ
    dstep = self.domain.dsplit
    pstep = self.domain.psplit
    
    offtstep = self.meteo.offtstep
    
    # Time steps per day
    freq = '{:.0f}s'.format(offtstep / min([dstep, pstep]))
    
    # List of time steps
    self.tstep_dates = \
        {ddi: date_range(ddi, ddf, period=freq)
         for ddi, ddf in zip(self.subsimu_dates[:-1],
                             self.subsimu_dates[1:])}

    # List of input dates
    # TODO: make the date inputs flexible (daily so far)
    self.input_dates = \
        {ddi: date_range(ddi, ddf, period='1D')
         for ddi, ddf in zip(self.subsimu_dates[:-1],
                             self.subsimu_dates[1:])}
    
    # Merged list of time steps
    self.tstep_all = date_range(datei, datef,
                                period=self.periods, subperiod=freq)
