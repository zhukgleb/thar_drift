import numpy as np
from astropy.io import fits
import os


def analyze_folder(path2data: str) -> list:
    thar_list = []
    for file in os.listdir(path2data):
        try:
            if isitthar(path2data + file):
                thar_list.append(path2data + file)
        except OSError:
            pass

    return thar_list


def isitthar(path2fits: str) -> bool:
    with fits.open(path2fits) as hdul:
        header = hdul[0].header
        if header['IMAGETYP'] == 'thar':
            return True
        else:
            False
        


if __name__ == "__main__":
    analyze_folder("/home/lambda/ccd/archive/20210224/")