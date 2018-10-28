# import pylab
import numpy as np
import matplotlib.pyplot as plt


def read_file(file="txt_files/upsilons-mass-xaa.txt"):
    data = np.genfromtxt(file)
    return data


def plot_hist(data, bins=225, title="", x_lab="", y_lab="", show=False, save=False, sv_nm="Upsilons_his.pdf"):
    n, bins, patches = plt.hist(data, bins=bins) # , density=True)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.title(title)
    if save:
        plt.savefig(sv_nm)
    if show:
        plt.show()
    return n, bins, patches


def find_stupid_peak(x, y, min_index, max_index):
    y_max = y[min]  # you cant call variables min or max because they are key words
    for i in range(x[min], x[max]): # min_index is the index of the x bin at the minimum position
        if y[i] >= y[i-1]:
            y_max = y[i]
    return y_max


def noise_check(y, peaks, per=5):
    rem = []
    smoothing = int(len(y)*per/100)
    for i in range(len(peaks)-1):
        if np.isclose(a=peaks[i], b=peaks[i+1], atol=smoothing):
            rem.append(i)  # not removing the 1st cause of the noise
        elif not np.isclose(a=y[i], b=y[i+1], atol=0.1*y[i]):  # attempt to remove massive spikes
            rem.append(i)
    for i in sorted(rem, reverse=True):
        del peaks[i]
    del peaks[len(peaks)-1]  # Removes the last data. This works for this data but possibly not generally :'(
    return peaks


def find_peak(x, y, smoothing=3, percentage_peak=15, show_peaks=True, save=False, sv_nm="muon_with_peaks.pdf"):
    per = 1 + percentage_peak / 100
    smoothing = int(len(y) * smoothing/100)
    peaks = []
    peak_found = False
    for i in range(smoothing, len(y)-1):
        if i + smoothing < len(y):
            next_avg = np.average(y[i:i+smoothing])
        elif i + smoothing >= len(y):
            next_avg = len(y) - i  # Maybe need -1

        prev_avg = np.average(y[i-smoothing:i])

        if peak_found and y[i] < y[i+1]:
            peak_found = False

        if y[i] > next_avg * per and y[i] > prev_avg and not peak_found:
            peaks.append(i)
            peak_found = True

    peaks = noise_check(y, peaks)
    x_new = [x[i] for i in peaks]
    y_new = [y[i] for i in peaks]
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
