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
    sb_data = []
    for file in biases_list: 
        bias_data.append(get_bias(file))
        sb_data.append(get_bias(file)[0])

    
    sb = sum(sb_data) / len(sb_data)
    return sb, bias_data

def get_dark(path2dark: str, sb):
    with fits.open(path2dark) as hdul:
            d = hdul[0].data
            exp = hdul[0].header
            exp = int(exp['EXPTIME'])

    return d, np.mean(d), np.min(d), np.max(d), np.std(d), exp


def get_dark_stats(path2darks: str, sb):
    darks_list = make_fits_list(path2darks)
    darks_data = []
    for file in darks_list:
        darks_data.append(get_dark(file, sb))
        

    
    return darks_data
   


if __name__ == "__main__":
    sb, b_data = get_superbias("/home/alpha/thar_drift/data/bias/")
    dd = get_dark_stats("/home/alpha/thar_drift/data/dark/", sb)
    photon_in_seconds = [dark[1] / dark[-1] for dark in dd]
    print(photon_in_seconds)
