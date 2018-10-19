# import pylab
import numpy as np
import matplotlib.pyplot as plt


def read_file(file="upsilons-mass-xaa.txt"):
    data = np.genfromtxt(file)
    return data


def plot_hist(data, title="", x_lab="", y_lab="", show=False, save=False, sv_nm="Upsilons_his.pdf"):
    n, bins, patches = plt.hist(data, bins=100, density=True)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.title(title)
    if save:
        plt.savefig(sv_nm)
    if show:
        plt.show()
    return n, bins, patches


def find_peak(x, y, percentage_peak=5):  # have a bit that if its mor than a certain % up then peak there
    per = 1 + percentage_peak / 100
    peaks = []
    print(len(y))
    for i in range(1, len(y)-1):
        if y[i] > y[i-1]*per and y[i+1] < y[i]:
            peaks.append(i)

    print(peaks)
    x_new = [x[i] for i in range(len(peaks))]
    print(x[peaks[5]])
    print(x_new)
    y_new = [y[i] for i in range(len(peaks))]
    plt.plot(x_new, y_new, 'o')
    plt.show()
    max_y = np.argmax(y)


def main():
    data = read_file()
    n, bins, patches = plot_hist(data, title="Upsilons Mass", x_lab="Mass ($GeV/c^2$)", y_lab="Frequency")
    # bin_data = zip(bins[:-1], n)
    # print(bin_data[0])
    find_peak(x=bins[:-1], y=n)

main()

# entries, binedges, patches = pylab.hist(xmass, bins = Nbins, range = [binMin,binMax])
