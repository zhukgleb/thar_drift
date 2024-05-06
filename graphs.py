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
    data = get_thar_shifts("opt_data.txt")
    data_nes = get_thar_shifts("opt_data_NES.txt")


    with plt.style.context(['retro', 'grid']):
        fig, ax = plt.subplots(nrows=2)
        ax[0].scatter(data[:, 0], data[:, 1])
        ax[1].scatter(data_nes[:, 0], data_nes[:, 1])
        plt.show()
