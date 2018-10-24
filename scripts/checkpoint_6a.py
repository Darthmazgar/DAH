# import pylab
import numpy as np
import matplotlib.pyplot as plt


def read_file(file="txt_files/upsilons-mass-xaa.txt"):
    data = np.genfromtxt(file)
    return data


def plot_hist(data, title="", x_lab="", y_lab="", show=False, save=False, sv_nm="Upsilons_his.pdf"):
    n, bins, patches = plt.hist(data, bins=150) # , density=True)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.title(title)
    if save:
        plt.savefig(sv_nm)
    if show:
        plt.show()
    return n, bins, patches


def find_stupid_peak(x, y, min_index, max_index):
    y_max = y[min]
    for i in range(x[min], x[max]): # min_index is the index of the x bin at the minimum position
        if y[i] >= y[i-1]:
            y_max = y[i]
    return y_max


def find_peak(x, y, smoothing=3, percentage_peak=10, show_peaks=True, save=False, sv_nm="muon_with_peaks.pdf"):
    per = 1 + percentage_peak / 100
    peaks = []
    peak_found = False
    for i in range(1, len(y)-1):
        if i + smoothing < len(y):
            next_avg = np.average(y[i:i+smoothing])
        elif i + smoothing >= len(y):
            next_avg = len(y) - i  # Maybe need -1
        else:
            next_avg = y[i+1]  # Contingency

        if peak_found and y[i] < y[i+1]:
            peak_found = False

        if y[i] > next_avg * per and y[i+1] < y[i] and not peak_found:
            peaks.append(i)
            peak_found = True
    x_new = [x[i] for i in peaks]
    y_new = [y[i] for i in peaks]
    # peak_coords = set(zip(x_new, y_new))  Probably don't need
    peak_masses = x_new
    if show_peaks:
        plt.plot(x_new, y_new, 'o')
        if save:
            plt.savefig(sv_nm)
        plt.show()
    return peak_masses, peaks


def main():
    data = read_file()
    n, bins, patches = plot_hist(data, title="Muon Pair Masses", x_lab="Mass ($GeV/c^2$)", y_lab="Frequency")
    peak_masses, peak_index = find_peak(x=bins[:-1], y=n)
    # stupid_peak = find_stupid_peak(x=bins[:-1], y=n)
    # differences = peak_masses - peak_masses[0]
    # print("The muon pair masses are: %.3f, %.3f and %.3f GeV." % (peak_masses[0], peak_masses[1], peak_masses[2]))
    # print("The Muon mass differences are: %.3f and %.3f GeV." %(differences[1], differences[2]))
    # mins = peak_analysis(data, peak_index)peak_location
    # print(mins)


main()

# entries, binedges, patches = pylab.hist(xmass, bins = Nbins, range = [binMin,binMax])
