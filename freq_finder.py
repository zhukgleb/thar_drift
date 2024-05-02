import numpy as np
from astropy.timeseries import LombScargle

def LS(t: np.ndarray, y: np.ndarray):
    ls = LombScargle(t, y)
    freq, power = ls.autopower()
    return freq, power
