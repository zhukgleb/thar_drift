import numpy as np
from astropy.timeseries import LombScargle


def LS(t: np.ndarray, y: np.ndarray):
    ls = LombScargle(t, y)
    freq, power = ls.autopower()
    return freq, power


def calc_phase(t: np.ndarray, period: float):
    """Make a phase plot for period serching...

    Parameters
    ----------
    t : ndarray
        time array
    period : float
        period value in freq unit

    Returns
    -------
    phase : ndarray
        just a phase array
    """

    return (t / period) % 1  #haha, so simple...

