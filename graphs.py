import matplotlib.pyplot as plt
import numpy as np
import scienceplots
from matplotlib import rc

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
#    shift_data = get_thar_shifts("opt_data.txt")
    # plt.plot(pd[:, 0], pd[:, 6])
#    plt.plot(shift_data[:, 0], shift_data[:, 1])
#    plt.show()
