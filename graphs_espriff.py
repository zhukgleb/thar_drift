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
    save = False
    show = True

    data = get_thar_shifts("opt_data_esp_reverse.txt")
    f, p = LS(data["mjd"], data["x_shift"])
    period_days = 1.0 / f
    period_hours = period_days * 24
    best_period = period_days[np.argmax(p)]
    phase = calc_phase(data["mjd"], best_period * 24)

    with plt.style.context(["retro", "grid"]):
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
        ax.scatter(data["z"], data["x_shift"], label="Dispersion axis", marker="D")
        ax.plot(data["z"], data["x_shift"])
        ax.scatter(data["z"], data["y_shift"], label="Order axis", marker="s")
        ax.plot(data["z"], data["y_shift"])
        plt.legend()
        plt.tight_layout()
        if show:
            plt.show()
        if save:
            plt.savefig("figures/flex.pdf")

        # Good data for demo's is from 60430.2 to 60430.6
        # Have a exponential grove and liniear plato
        from scipy import stats

        # Coord drift

        #        plt.plot(data["x_shift"], data[:, 2])
        #        plt.show()
        #        plt.plot(data["mjd"], data[:, 4])
        #        plt.show()

        # Diffirence graph
#        max_x_diff_fits = data[np.where(data["x_shift"] == max(data["x_shift"]))]
#        min_x_diff_fits = data[np.where(data["x_shift"] == min(data["x_shift"]))]
#        min_x_data = get_data_from_fits_esp(min_x_diff_fits["fname"][0])
#        max_x_data = get_data_from_fits_esp(max_x_diff_fits["fname"][0])

#        diff_data = max_x_data - min_x_data

#       fig, ax = plt.subplots(figsize=(8, 6), ncols=2)

#       ax[0].imshow(diff_data)
#       levels = np.linspace(diff_data.min(), diff_data.max(), 50)  # 5 levels
#       contour = ax[1].contour(
#           diff_data, levels=levels, cmap="viridis", linewidths=1.5
#       )
#       fig.colorbar(contour, ax=ax[1])  # Добавление цветовой шкалы к первому графику
#       ax[1].invert_yaxis()
#       if show:
#           plt.show()
