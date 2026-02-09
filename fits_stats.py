from astropy.io import fits
from sklearn.preprocessing import Normalizer
from grabber import make_fits_list
import numpy as np



def get_bias(path2bias: str):
    with fits.open(path2bias) as hdul:
            d = hdul[0].data
    return d, np.mean(d), np.min(d), np.max(d), np.std(d)


def get_superbias(path2biases: str):
    biases_list = make_fits_list(path2biases)
    bias_data = []
    for file in biases_list: 
        bias_data.append(get_bias(file))
        
    print(bias_data)




if __name__ == "__main__":
    get_superbias("/home/alpha/thar_drift/data/bias/")
