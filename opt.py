import matplotlib.pyplot as plt

from skimage import data, color
from scipy import ndimage as ndi
import numpy as np

astronaut = color.rgb2gray(data.astronaut())
shifted = ndi.shift(astronaut, (0, 50))
fig, axes = plt.subplots(nrows=1, ncols=2)
axes[0].imshow(astronaut)
axes[0].set_title('Оригинальное')
axes[1].imshow(shifted)
axes[1].set_title('Смещенное')

def mse(arr1, arr2):
    return np.mean((arr1 - arr2)**2)

ncol = astronaut.shape[1]
# Покрыть расстояние в 90% от длины в столбцах,
# с одним значением в расчете на процентный пункт
shifts = np.linspace(-0.5 * ncol, 0.5 * ncol, len(astronaut))
mse_costs = []
for shift in shifts:
    shifted_back = ndi.shift(shifted, (0, shift))
    mse_costs.append(mse(astronaut, shifted_back))

from scipy import optimize

def astronaut_shift_error(shift):
    corrected = ndi.shift(shifted, (0, shift))
    return mse(astronaut, corrected)

res = optimize.minimize(astronaut_shift_error, 0, method='Nelder-Mead')
#print(f'Оптимальный сдвиг для коррекции составляет: {res.x}')
