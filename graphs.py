import matplotlib.pyplot as plt
import numpy as np
import scienceplots
from matplotlib import rc

plt.style.use("science")
font = {'family' : 'normal',
        'size': 16}

rc('font', **font)

def get_thar_shifts(filename: str) -> np.array:
    data = np.genfromtxt(filename)
    data = data[data[:, 0].argsort()]
    return data


if __name__ == "__main__":
    pd = np.genfromtxt("parsed_data.txt")
    shift_data = get_thar_shifts("opt_data.txt")
    # plt.plot(pd[:, 0], pd[:, 6])
    plt.plot(shift_data[:, 0], shift_data[:, 1])
    plt.show()