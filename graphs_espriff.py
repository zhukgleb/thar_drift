import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
from freq_finder import LS, calc_phase
from scipy.signal import find_peaks
import matplotlib.ticker as ticker
import matplotlib.ticker as plticker
import scienceplots
from grabber import get_data_from_fits, get_data_from_fits_esp


plt.style.use("science")
font = {"family": "normal", "size": 16}

rc("font", **font)


def get_thar_shifts(filename: str) -> np.ndarray:
    data = np.genfromtxt(
        filename,
        delimiter="\t",
        dtype=[
            ("mjd", float),
            ("z", float),
            ("x_shift", float),
            ("y_shift", float),
            ("angle", float),
            ("mre", float),
            ("fname", "U80"),
        ],
    )

    data = np.sort(data, order="mjd")
    return data


def get_meteo(
    mjd_start: float, mjd_end: float, f_name: str = "parsed_data.txt"
) -> np.ndarray:
    meteo_data = np.genfromtxt(f_name)
    return meteo_data[
        np.where((meteo_data["mjd"] >= mjd_start) & (meteo_data["mjd"] <= mjd_end))
    ]


if __name__ == "__main__":
    save = True
    show = False

    data = get_thar_shifts("opt_data_esp_reverse.txt")
    f, p = LS(data["mjd"], data["x_shift"])
    period_days = 1.0 / f
    period_hours = period_days * 24
    best_period = period_days[np.argmax(p)]
    phase = calc_phase(data["mjd"], best_period * 24)

    with plt.style.context(["science", "grid"]):
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(data["mjd"], data["x_shift"], label="Dispersion axis", color="navy")
        ax.scatter(data["mjd"], data["y_shift"], label="Order axis", color="crimson")
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%0.1f"))
        loc = plticker.MultipleLocator(base=0.01)
        #
        ax.xaxis.set_major_locator(loc)
        plt.title("Shift spread")
        plt.xlabel("MJD")
        plt.ylabel("Shift, px")
        plt.legend()
        plt.tight_layout()
        if save:
            plt.savefig("figures/shifts.pdf")
        if show:
            plt.show()

        # Z vs shift
        #
        #

        fig, ax = plt.subplots(figsize=(6, 6))

        plt.title("Total flexure of ESPriF")
        plt.xlabel("Zenith distance")
        plt.ylabel("Shift, px")
        ax.scatter(data["z"], data["x_shift"], label="Dispersion axis", marker="D", color="crimson")
        ax.plot(data["z"], data["x_shift"], color="crimson")
        ax.scatter(data["z"], data["y_shift"], label="Order axis", marker="s", color="navy")
        ax.plot(data["z"], data["y_shift"], color="navy")
        plt.legend()
        plt.tight_layout()
        if show:
            plt.show()
        if save:
            plt.savefig("figures/flex.pdf")


        from scipy import stats

        # Coord drift

        #        plt.plot(data["x_shift"], data[:, 2])
        #        plt.show()
        #        plt.plot(data["mjd"], data[:, 4])
        #        plt.show()

        # Diffirence graph
    with plt.style.context(["science"]):

        max_x_diff_fits = data[np.where(data["x_shift"] == max(data["x_shift"]))]
        min_x_diff_fits = data[np.where(data["x_shift"] == min(data["x_shift"]))]
        min_x_data = get_data_from_fits_esp(min_x_diff_fits["fname"][0])
        max_x_data = get_data_from_fits_esp(max_x_diff_fits["fname"][0])

        diff_data = max_x_data - min_x_data

        fig, ax = plt.subplots(figsize=(8, 12), ncols=2)
        print(diff_data[1000:1200])
        cax = ax[0].imshow(diff_data)
        cax = ax[1].imshow(diff_data[1000:1200, 1000:1200])
        ax[0].set_title("Max shift - min shift difference")
        ax[1].set_title("Local difference")
        plt.tight_layout()
        if show:
            plt.show()
        if save:
            plt.savefig("figures/diffmapx.pdf")
