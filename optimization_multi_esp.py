import numpy as np
from skimage import transform
import os
from astropy.io import fits
from sklearn.preprocessing import Normalizer
from astropy.time import Time
from datetime import datetime as dt
from grabber import analyze_folder, make_fits_list
from opt_func import align
from multiprocessing import Pool, cpu_count

# Raw introduction....
# fits_list = os.listdir("/home/lambda/ccd/archive/20240424/")

fits_list = []
# archive_path = "/home/alpha/ccd/archive/20240428/"
archive_path = "/home/alpha/thar_drift/data/espriff/"
# archive_path = "/home/lambda/20240428/"

# for night in os.listdir(archive_path):
fits_list.append(make_fits_list(archive_path))

# Flatten the list
fits_list = fits_list[0]

reap = fits_list.index("/home/alpha/thar_drift/data/espriff/Be20260202_016t.fits")
# reap = fits_list.index("/home/lambda/20240428/Bn20240428_007.fts")

data_list = []
mjd_list = []
z_list = []

with fits.open(fits_list[reap]) as hdul:
    d = hdul[0].data
    print(d)
    transformer = Normalizer().fit(
        d
    )  # Do normalization [0, 1] for adequate mse estimation
    header = hdul[0].header
    native = dt.strptime(header["DATE"].split(".")[0], "%Y-%m-%dT%H:%M:%S")
    mjd_list.append(Time(native, scale="local").mjd)
    z_list.append(header["Z"])
    d = transformer.transform(d)
    data_list.append(d)
    rep_fits = d
    print(f"reap fits is: {fits_list[reap]}")

xo_arr = []
yo_arr = []
opt_data = []


def process_file(file):
    with fits.open(file) as hdul:
        # print(file)
        d = hdul[0].data
        transformer = Normalizer().fit(
            d
        )  # Do normalization [0, 1] for adequate mse estimation
        header = hdul[0].header
        native = dt.strptime(header["DATE"].split(".")[0], "%Y-%m-%dT%H:%M:%S")
        mjd = Time(native, scale="local").mjd
        z = header["Z"]
        d = transformer.transform(d)
        if len(d[0]) * 1.1 < len(rep_fits[0]):
            d = d.T
        # print(d.shape)
        shifted = d
        tf, xo, yo, ang, mre = align(rep_fits, d, method="BH")
        corrected = transform.warp(shifted, tf, order=3)
        return mjd, z, xo, yo, ang, mre, file


def write_to_file(result):
    mjd, z, xo, yo, ang, mre, fname = result
    with open("opt_data_esp_reverse.txt", "a") as f:
        f.write(f"{mjd}\t{z}\t{xo}\t{yo}\t{ang}\t{mre}\t{fname}\n")


# Using Pool from multiprocessing to parallelize file processing
files_done = 0
if __name__ == "__main__":
    with Pool(processes=cpu_count()) as pool:
        for result in pool.imap(process_file, fits_list[1:]):
            write_to_file(result)
            files_done += 1
            print(f"{files_done / len(fits_list) * 100} %", end="\r")
