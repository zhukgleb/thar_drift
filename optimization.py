import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import ndimage as ndi
from skimage import transform
import os
from astropy.io import fits
from sklearn.preprocessing import Normalizer
from astropy.time import Time
from datetime import datetime as dt
from grabber import analyze_folder

# Raw introduction....
# fits_list = os.listdir("/home/lambda/ccd/archive/20240424/")

fits_list_comp = []
archive_path = "/home/lambda/ccd/archive/"

for night in os.listdir(archive_path):
    print(archive_path + night)
    fits_list_comp.append(analyze_folder(archive_path + night + "/"))

fits_list = []  # Now flat'n our list
for sublist in fits_list_comp:
    for val in sublist:
        fits_list.append(val)

del fits_list_comp
print(fits_list)

data_list = []
mjd_list = []


for i in range(len(fits_list)):
    with fits.open(fits_list[i]) as hdul:
        d = hdul[0].data[0]
        transformer = Normalizer().fit(d)  # Do normalization [0, 1] for adequate mse estimation
        header = hdul[0].header
        native = dt.strptime(header['DATE'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
        mjd_list.append(Time(native, scale="local").mjd)
        d = transformer.transform(d)
        data_list.append(d)
        print(d.shape)
        
rep_fits = data_list[0]

for i in range(len(data_list)):
    if len(data_list[i][0]) * 1.1 < len(rep_fits[0]):
        data_list[i] = data_list[i].T


def mse(arr1, arr2):
    """Compute the mean squared error between two arrays."""
    return np.mean((arr1 - arr2)**2)


# Not good to use global rep point, but...
def rep_fits_shift_error(shift, image):
    corrected = ndi.shift(image, (0, shift))
    return mse(rep_fits, corrected)


def downsample2x(image):
    offsets = [((s + 1) % 2) / 2 for s in image.shape]
    slices = [slice(offset, end, 2)
              for offset, end in zip(offsets, image.shape)]
    coords = np.mgrid[slices]
    return ndi.map_coordinates(image, coords, order=1)


def gaussian_pyramid(image, levels=6):
    """Make a Gaussian image pyramid.

    Parameters
    ----------
    image : array of float
        The input image.
    max_layer : int, optional
        The number of levels in the pyramid.

    Returns
    -------
    pyramid : iterator of array of float
        An iterator of Gaussian pyramid levels, starting with the top
        (lowest resolution) level.
    """
    pyramid = [image]

    for level in range(levels - 1):
        # blurred = ndi.gaussian_filter(image, sigma=2/3)
        image = downsample2x(image)
        pyramid.append(image)

    return reversed(pyramid)


def make_rigid_transform(param):
    r, tc, tr = param
    return transform.SimilarityTransform(rotation=r,
                                         translation=(tc, tr))


def cost_mse(param, reference_image, target_image):
    transformation = make_rigid_transform(param)
    transformed = transform.warp(target_image, transformation, order=3, output_shape=(reference_image.shape[0], reference_image.shape[1]))
    return mse(reference_image, transformed)


def align(reference, target, cost=cost_mse, nlevels=7, method='Powell'):
    pyramid_ref = gaussian_pyramid(reference, levels=nlevels)
    pyramid_tgt = gaussian_pyramid(target, levels=nlevels)

    levels = range(nlevels, 0, -1)
    image_pairs = zip(pyramid_ref, pyramid_tgt)

    p = np.zeros(3)

    for n, (ref, tgt) in zip(levels, image_pairs):
        p[1:] *= 2
        if method.upper() == 'BH':
            res = optimize.basinhopping(cost, p,
                                        minimizer_kwargs={'args': (ref, tgt)})
            if n <= 4:  # avoid basin-hopping in lower levels
                method = 'Powell'
        else:
            res = optimize.minimize(cost, p, args=(ref, tgt), method='Powell')
        p = res.x
        # print current level, overwriting each time (like a progress bar)
        print(f'Level: {n}, Angle: {np.rad2deg(res.x[0]) :.3}, '
              f'Offset: ({res.x[1] * 2**n :.3}, {res.x[2] * 2**n :.3}), '
              f'Cost: {res.fun :.3}', end='\r')
    xo = res.x[1] * 2
    yo = res.x[2] * 2
    ang = np.rad2deg(res.x[0])
    mre = res.fun
    print('')  # newline when alignment complete
    return make_rigid_transform(p), xo, yo, ang, mre


xo_arr = []
yo_arr = []

opt_data = []
for i in range(0, len(data_list)):
    shifted = data_list[i]
    tf, xo, yo, ang, mre = align(rep_fits, shifted)
    corrected = transform.warp(shifted, tf, order=3)
    xo_arr.append(xo)
    yo_arr.append(yo)
    opt_data.append([mjd_list[i], xo, yo, ang, mre])
    

np.savetxt("opt_data.txt", opt_data)