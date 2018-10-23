# import pylab
import numpy as np
import matplotlib.pyplot as plt


def read_file(file="txt_files/upsilons-mass-xaa.txt"):
    data = np.genfromtxt(file)
    return data


def plot_hist(data, title="", x_lab="", y_lab="", show=False, save=False, sv_nm="Upsilons_his.pdf"):
    n, bins, patches = plt.hist(data, bins=50, density=True)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.title(title)
    if save:
        plt.savefig(sv_nm)
    if show:
        plt.show()
    return n, bins, patches


def find_peak(x, y, percentage_peak=15, show_peaks=True):
    per = 1 + percentage_peak / 100
    peaks = []
    for i in range(2, len(y)-1):
        if y[i] > y[i-2]*per and y[i+1] < y[i]:
            peaks.append(i)
    x_new = [x[i] for i in peaks]
    y_new = [y[i] for i in peaks]
    peak_coords = set(zip(x_new, y_new))  # Probably don't need
    peak_masses = x_new
    if show_peaks:
        plt.plot(x_new, y_new, 'o')
        plt.show()
    return peak_masses


def main():
    data = read_file()
    n, bins, patches = plot_hist(data, title="Upsilons Mass", x_lab="Mass ($GeV/c^2$)", y_lab="Frequency")
    peak_masses = find_peak(x=bins[:-1], y=n)
    print("The masses of upsilon 1, upsilon 2 and upsilon 3 are %.3f, %.3f and %.3f GeV respectively." % (peak_masses[0], peak_masses[1], peak_masses[2]))

main()

# entries, binedges, patches = pylab.hist(xmass, bins = Nbins, range = [binMin,binMax])
