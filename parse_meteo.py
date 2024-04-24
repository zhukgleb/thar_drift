import matplotlib.pyplot as plt
import numpy as np
import os
from astropy.time import Time
from datetime import datetime as dt
import pytz

# Yep, wild imports, but i don't have endless time to fancy code

meteo_list = os.listdir("meteo/")

# Convert date and time to mod. Julian time
# I don't give a fuck
def date_to_mjd(date, time):
    full_time = date + " " + time
    native = dt.strptime(full_time, "%d-%b-%Y %H:%M:%S")
    local = pytz.timezone("Europe/Moscow")
    local_dt = local.localize(native)
    utc_dt = local_dt.astimezone(pytz.utc)
    ut = Time(utc_dt, scale="local")
    mjd = ut.mjd
    return mjd


# Extract data from one data file
def xtract_meteo(path2file):
    data = np.genfromtxt(path2file, dtype=str, invalid_raise = False)
    date = data[:, 0]
    time = data[:, 1]
    t_out = data[:, 3].astype(float)
    t_in = data[:, 4].astype(float)
    t_mir = data[:, 5].astype(float)
    pressure = data[:, 6].astype(float)
    wind = data[:, 7].astype(float)
    hum = data[:, 8].astype(float)
    del data
    mjd = []
    for i in range(len(date)):
        mjd.append(date_to_mjd(date[i], time[i]))

    mjd = np.array(mjd).astype(float)
    # I hope all this garbage is gone out of function....
    return np.column_stack((mjd, t_out, t_in, t_mir, pressure, wind, hum))
    

if __name__ == "__main__":
    all_data = []
    for i in range(0, len(meteo_list)):
        all_data.append(xtract_meteo("meteo/" + meteo_list[i]))
        print(i/len(meteo_list) * 100, "%", end='\r')
    all_data = np.concatenate(all_data)
    all_data = all_data[all_data[:, 0].argsort()]
    # plt.plot(all_data[:, 0], all_data[:, 1])
    # plt.show()
    np.savetxt("parsed_data.txt", all_data)

