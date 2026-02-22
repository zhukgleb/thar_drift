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
            print(d)
            exp = hdul[0].header
            exp = int(exp['EXPTIME'])
            d = d - sb
            print(d)


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


    import matplotlib.pyplot as plt
    from matplotlib.colors import LogNorm
    import scienceplots

    with plt.style.context("science"):
        fig, ax = plt.subplots(figsize=(6, 6))
        plt.title("Mean bias")
        plt.tight_layout()

        cax = ax.imshow(sb, norm=LogNorm())

        cbar = fig.colorbar(cax)


        table_text =  f'Mean: {np.mean(sb):.3f}\n STD: {np.std(sb):.3f}\n'

        bbox_props = dict(boxstyle="round,pad=0.3",
                        facecolor="white",
                        edgecolor="black",
                        linewidth=2,
                        alpha=0.9)

        ax.text(0.05, 0.95, table_text,
                transform=ax.transAxes,
                fontsize=11,
                verticalalignment='top',
                bbox=bbox_props)

        # plt.savefig('figures/bias.pdf')
        plt.show()


        
        fig, ax = plt.subplots(figsize=(4, 4))
        plt.tight_layout()
        plt.title("Thermal electrons")
        ax.scatter(np.arange(1, len(photon_in_seconds)+1), photon_in_seconds, color="black", alpha=0.8)
        plt.xlabel("Exposition number")
        plt.ylabel("Photon per second")
        
        plt.tight_layout()
        plt.savefig("figures/darks.pdf")
        plt.show()
