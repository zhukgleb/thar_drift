import matplotlib.pyplot as plt
import numpy as np
import scienceplots
from matplotlib import rc

plt.style.use("science")
font = {'family' : 'normal',
        'size': 16}

rc('font', **font)

if __name__ == "__main__":
    pd = np.genfromtxt("parsed_data.txt")
    plt.plot(pd[:, 0], pd[:, 6])
    plt.show()