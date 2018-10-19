# import pylab
import numpy as np
import matplotlib.pyplot as plt


def read_file(file="upsilons-mass-xaa.txt"):
    data = np.genfromtxt(file)
    return data

def plot_hist(data, title="", x_lab="", y_lab="", save=False, sv_nm="Upsilons_his.pdf"):
    plt.hist(data)
    plt.show()


def main():
    data = read_file()
    plot_hist(data)

main()

# entries, binedges, patches = pylab.hist(xmass, bins = Nbins, range = [binMin,binMax])
