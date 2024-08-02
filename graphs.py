import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from freq_finder import LS, calc_phase
from scipy.signal import find_peaks
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker
import scienceplots


plt.style.use("science")
font = {'family' : 'normal',
        'size': 16}

rc('font', **font)

def get_thar_shifts(filename: str) -> np.ndarray:
    data = np.genfromtxt(filename, delimiter='\t', dtype=[('mjd', float), ('x_shift', float), ('y_shift', float), ('angle', float), ('mre', float), ('fname', 'U60')])
 
    data = np.sort(data, order='mjd')
    return data


def get_meteo(mjd_start: float, mjd_end: float, f_name: str="parsed_data.txt") -> np.ndarray:
    meteo_data = np.genfromtxt(f_name)
    return meteo_data[np.where((meteo_data['mjd'] >= mjd_start) & 
                               (meteo_data['mjd'] <=mjd_end))]


if __name__ == "__main__":
    save = False
    data = get_thar_shifts("opt_data.txt")
    print(data)
    f, p = LS(data["mjd"], data["x_shift"])
    period_days = 1. / f
    period_hours = period_days * 24
    best_period = period_days[np.argmax(p)]
    phase = calc_phase(data['mjd'], best_period * 24)


    with plt.style.context(['retro', 'grid']):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(data["mjd"], data["x_shift"], label="Order axis", color="navy")
        ax.scatter(data["mjd"], data["y_shift"], label="Dispersion axis", color="crimson")
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        loc = plticker.MultipleLocator(base=0.3)
        ax.xaxis.set_major_locator(loc)
        plt.title("Shift spread")
        plt.xlabel("MJD")
        plt.ylabel("Shift, px")
        plt.legend()
        plt.tight_layout()
        if save:
            plt.savefig("figures/shifts.pdf")
        else:
            plt.show()

        # Good data for demo's is from 60430.2 to 60430.6
        # Have a exponential grove and liniear plato
        from scipy import stats
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.title("Night shifts")
        good_data = np.where((data["mjd"] >= 60430.25) & (data["mjd"] <= 60430.57))
        not_so_good_data = np.where((data["mjd"] >= 60430.2) & (data["mjd"] <= 60430.6))
        slope, intercept, r_value, p_value, std_err = stats.linregress(data["mjd"][good_data], data["x_shift"][good_data])
        plt.plot(data["mjd"][not_so_good_data], slope*data["mjd"][not_so_good_data] + intercept, '--', color='black', label='Linear regression', linewidth=2)  # Regression line
        plt.scatter(data["mjd"][not_so_good_data], data["x_shift"][not_so_good_data], color='black', label="Not calm state")
        plt.scatter(data["mjd"][good_data], data["x_shift"][good_data], color='#009E73', label="Calm state")  # Line part
        line_params = f'k = {slope:.2f}'
        time = r'$\mathit{85~min}$'
        # plt.text(1, 12, params_label, fontsize=12, color="blue")
        props = dict(boxstyle='round', facecolor='white', alpha=0.5)
        plt.text(data["mjd"][good_data][2], 5, line_params, bbox=props)
        plt.text(data["mjd"][not_so_good_data][4], 4, time, rotation='vertical')
        plt.text(data["mjd"][not_so_good_data][-3], 4, time, rotation='vertical')
        ax.axvspan(data["mjd"][not_so_good_data][0] - 0.01, data["mjd"][good_data][0], facecolor='yellow', alpha=0.5)
        ax.axvspan(data["mjd"][not_so_good_data][-1] + 0.025, data["mjd"][good_data][-1], facecolor='yellow', alpha=0.5)
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        loc = plticker.MultipleLocator(base=0.1)
        plt.xlabel("MJD")
        plt.ylabel("Shift, px")
        plt.legend()
        plt.tight_layout()
        if save:
            plt.savefig("figures/night_shifts.pdf")
        else:
            plt.show()



        # A Complex two line graph
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.title("Night shifts")
        good_data = np.where((data["mjd"] >= 60429.62) & (data["mjd"] <= 60430.18))
        not_so_good_data = np.where((data["mjd"] >= 60429.5) & (data["mjd"] <= 60430.3))
        slope_x, intercept_x, r_value_x, p_value_x, std_err_x = stats.linregress(data["mjd"][good_data], data["x_shift"][good_data])
        slope_y, intercept_y, r_value_y, p_value_y, std_err_y = stats.linregress(data["mjd"][good_data], data["y_shift"][good_data])

        # Regression part
        plt.plot(data["mjd"][not_so_good_data], slope_x*data["mjd"][not_so_good_data] + intercept_x, '--', color='#1e8cb0', label='Order regression', linewidth=2)  # Regression line
        plt.plot(data["mjd"][not_so_good_data], slope_y*data["mjd"][not_so_good_data] + intercept_y, '--', color='#e953da', label='Dispersion regression', linewidth=2) 
        
        # Data illustration part
        plt.scatter(data["mjd"][not_so_good_data], data["x_shift"][not_so_good_data], color='navy', label="Order axis")
        plt.scatter(data["mjd"][not_so_good_data], data["y_shift"][not_so_good_data], color='crimson', label="Dispersion axis")
        # plt.scatter(data["mjd"][good_data], data[:, 2][good_data], color='#009E73', label="Calm state")  # Line part
        
        line_params_x = f'Order line k = {slope_x:.2f}'
        line_params_y = f'Dispersion line k = {slope_y:.2f}'
        time = r'$\mathit{85~min}$'
        # plt.text(1, 12, params_label, fontsize=12, color="blue")
        props = dict(boxstyle='round', facecolor='white', alpha=0.5)
        plt.text(data["mjd"][good_data][2], 5.5, line_params_x, bbox=props)
        plt.text(data["mjd"][good_data][2], 4.7, line_params_y, bbox=props)

        plt.text(data["mjd"][not_so_good_data][4], 4, time, rotation='vertical')
        plt.text(data["mjd"][not_so_good_data][-3], 4.2, time, rotation='vertical')
        ax.axvspan(data["mjd"][not_so_good_data][0] - 0.01, data["mjd"][good_data][0], facecolor='yellow', alpha=0.5)
        ax.axvspan(data["mjd"][not_so_good_data][-1] + 0.025, data["mjd"][good_data][-1], facecolor='yellow', alpha=0.5)
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        loc = plticker.MultipleLocator(base=0.1)
        plt.xlabel("MJD")
        plt.ylabel("Shift, px")
        plt.legend()
        plt.tight_layout()
        if save:
            plt.savefig("figures/night_shifts_y.pdf")
        else:
            plt.show()


        # Lomb-Scargle periodogram and phase plot
        fig, ax = plt.subplots(figsize=(8, 6), nrows=2)
        ax[0].plot(f, p, color='black')
        ax[0].set_xlabel("Events per day")
        ax[0].set_ylabel("Power")
        ax[1].scatter(phase, data["x_shift"], color="black", alpha=0.9)
        ax[1].set_xlabel("Phase")
        ax[1].set_ylabel("Shift")
        plt.tight_layout()
        if save:
            plt.savefig("figures/psd.pdf")
        else:
            plt.show()

        
        # Coord drift

#        plt.plot(data["x_shift"], data[:, 2])
#        plt.show()
#        plt.plot(data["mjd"], data[:, 4])
#        plt.show()


        # Diffirence graph
        max_x_diff_fits = data[np.where(data["x_shift"] == max(data["x_shift"]))]
        min_x_diff_fits = data[np.where(data["x_shift"] == min(data["x_shift"]))]
        print(min_x_diff_fits, max_x_diff_fits)
