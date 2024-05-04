import matplotlib.pyplot as plt
import numpy as np
import scienceplots
from matplotlib import rc
from freq_finder import LS, calc_phase
from scipy.signal import find_peaks


plt.style.use("science")
font = {'family' : 'normal',
        'size': 16}

rc('font', **font)

def get_thar_shifts(filename: str) -> np.ndarray:
    data = np.genfromtxt(filename)
    data = data[data[:, 0].argsort()]
    return data


def get_meteo(mjd_start: float, mjd_end: float, f_name: str="parsed_data.txt") -> np.ndarray:
    meteo_data = np.genfromtxt(f_name)
    return meteo_data[np.where((meteo_data[:, 0] >= mjd_start) & 
                               (meteo_data[:, 0] <=mjd_end))]


if __name__ == "__main__":
#    pd = np.genfromtxt("parsed_data.txt")
    shift_data = get_thar_shifts("opt_data.txt")
    # plt.plot(pd[:, 0], pd[:, 6])
    pparam = dict(xlabel='Time, MJD', ylabel=r'Shift, pixels')
    f, p = LS(shift_data[:, 0], shift_data[:, 1])
    peaks, _ = find_peaks(p, prominence=0.03)
    phase = calc_phase(shift_data[:, 0], peaks[2])

    with plt.style.context(['retro', 'grid']):
        fig, ax = plt.subplots()
#        ax.scatter(shift_data[:, 0], shift_data[:, 1], color="crimson", label="X shift")
#        ax.plot(shift_data[:, 0], shift_data[:, 2], color="navy", label="Y shift")
#        ax.legend(title='Curves:')
        ax.autoscale(tight=True)
#        ax.set(**pparam)
        plt.scatter(shift_data[:, 0], phase)
#        plt.plot(f[peaks], p[peaks], "x")
        # plt.scatter(shift_data[:, 0], shift_data[:, 1])
        # plt.scatter(shift_data[:, 0], shift_data[:, 2])
        plt.show()
