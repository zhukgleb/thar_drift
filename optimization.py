import numpy as np
from skimage import transform
import os
from astropy.io import fits
from sklearn.preprocessing import Normalizer
from astropy.time import Time
from datetime import datetime as dt
from grabber import analyze_folder
from opt_func import align

# Raw introduction....
# fits_list = os.listdir("/home/lambda/ccd/archive/20240424/")

fits_list = []
archive_path = "/home/lambda/ccd/archive/20240428/"

#for night in os.listdir(archive_path):
fits_list.append(analyze_folder(archive_path + "/"))

# fits_list = []  # Now flat'n our list
# for sublist in fits_list_comp:
#     for val in sublist:
#         fits_list.append(val)
# del fits_list_comp
#fits_list = os.listdir(archive_path)
#fits_list = [archive_path + "/" + fits_list[i] for i in range(len(fits_list))]
fits_list = fits_list[0]
# reap = fits_list.index("/home/lambda/ccd/archive/tests/Bn20240428_007.fts")
reap = 0

data_list = []
mjd_list = []

with fits.open(fits_list[reap]) as hdul:
    d = hdul[0].data[0]
    transformer = Normalizer().fit(d)  # Do normalization [0, 1] for adequate mse estimation
    header = hdul[0].header
    native = dt.strptime(header['DATE'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
    mjd_list.append(Time(native, scale="local").mjd)
    d = transformer.transform(d)
    data_list.append(d)
    rep_fits = d
    print(f"reap fits is: {fits_list[reap]}")


xo_arr = []
yo_arr = []
opt_data = []
for i in range(1, len(fits_list)):
    with fits.open(fits_list[i]) as hdul:
        print(fits_list[i])
        d = hdul[0].data[0]
        transformer = Normalizer().fit(d)  # Do normalization [0, 1] for adequate mse estimation
        header = hdul[0].header
        native = dt.strptime(header['DATE'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
        mjd_list.append(Time(native, scale="local").mjd)
        d = transformer.transform(d)
        if len(d[0]) * 1.1 < len(rep_fits[0]):
            d = d.T
        print(d.shape)
        shifted = d
        tf, xo, yo, ang, mre = align(rep_fits, d)
        corrected = transform.warp(shifted, tf, order=3)
        xo_arr.append(xo)
        yo_arr.append(yo)
        opt_data.append([mjd_list[i], xo, yo, ang, mre])
    
    np.savetxt("opt_data.txt", opt_data)
