import numpy as np
import matplotlib.pyplot as plt


def read_file(file="txt_files/upsilons-mass-xaa.txt"):
    data = np.genfromtxt(file)
    return data


def plot_hist(data, bins=225, title="", x_lab="", y_lab="", show=False, save=False, sv_nm="Upsilons_his.pdf"):
    n, bins, patches = plt.hist(data, bins=bins)  # , density=True)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.title(title)
    if save:
        plt.savefig(sv_nm)
    if show:
        plt.show()
    return n, bins, patches


def noise_check(y, peaks, per=5):
    rem = []
    smoothing = int(len(y)*per/100)
    for i in range(len(peaks)-1):
        if np.isclose(a=peaks[i], b=peaks[i+1], atol=smoothing):
            rem.append(i)  # not removing the 1st cause of the noise
        elif not np.isclose(a=y[i], b=y[i+1], atol=0.1*y[i]):  # attempt to remove massive spikes
            rem.append(i)
        elif y[peaks[i]] < 400:  # Will only work fo this bin sizing
            rem.append(i)
    for i in sorted(rem, reverse=True):
        del peaks[i]
    del peaks[len(peaks)-1]  # Removes the last data. This works for this data but possibly not generally :'(

    return peaks


def find_peak(x, y, smoothing=3, percentage_peak=15, show_peaks=True, save=False, sv_nm="muon_with_peaks.pdf", show=False):
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
        if show:
            plt.show()
    return peak_masses, peaks


def peak_analysis(y_data, x_data, peak_index, disp_width=True):
    ranges = []
    indices = []
    for peak in peak_index:
        ind = peak
        next_less = True
        prev_less = True
        right_min = ind
        left_min = ind
        while next_less:
            # if y_data[ind] < np.average(y_data[ind: ind+2]):
            if y_data[ind] < np.average([y_data[ind+1], y_data[ind+2], y_data[ind+3]]):
                right_min = ind
                next_less = False
            ind += 1

        ind = peak  # Reset
        while prev_less:
            # if y_data[ind] < np.average(y_data[ind: ind-2]):  # could probs move these into the same loop
            if y_data[ind] < np.average([y_data[ind-1], y_data[ind-2], y_data[ind-3]]):

                left_min = ind
                prev_less = False
            ind -= 1
        ranges.append([x_data[left_min], x_data[right_min]])
        indices.append([left_min, right_min])
        if disp_width:
            plt.axvline(x_data[left_min], color='green', linewidth=.8)
            plt.axvline(x_data[right_min], color='green', linewidth=.8)

    return ranges, indices


def region_mean(x_data, ind_range):
    return np.average(x_data[ind_range[0]:ind_range[1]])


def region_variance(x_data, ind_range):
    return np.var(x_data[ind_range[0]:ind_range[1]])


def region_stdev(x_data, ind_range):
    return np.std(x_data[ind_range[0]:ind_range[1]])


def std_err_mean(stdev, n):
    return stdev / np.sqrt(n)


def FWHM(peak_ind, ind_range, y_data, x_data, disp_half_width=True):
    avg_min = np.average([y_data[ind_range[0]], y_data[ind_range[1]]])
    height = y_data[peak_ind] - avg_min  # To remove non flat minimums
    half_max = height / 2

    larger = True
    i = peak_ind
    j = peak_ind

    one_side = False
    while larger:
        if y_data[i] <= (half_max + avg_min):
            right_lim = i
            if one_side:
                larger = False
            else:
                one_side = True
        if y_data[j] <= (half_max + avg_min):
            left_lim = j
            if one_side:
                larger = False
            else:
                one_side = True
        i += 1
        j -= 1
    if disp_half_width:
        plt.axvline(x_data[right_lim], color='red', linewidth=.8)
        plt.axvline(x_data[left_lim], color='red', linewidth=.8)
        plt.show()

    width = x_data[right_lim] - x_data[left_lim]
    return width


def est_sigma(fwhm):
    return fwhm / 2.355


def main():
    data = read_file()
    n, bins, patches = plot_hist(data, title="Muon Pair Masses", x_lab="Mass ($GeV/c^2$)", y_lab="Frequency")
    peak_masses, peak_index = find_peak(x=bins[:-1], y=n)
    differences = peak_masses - peak_masses[0]
    print("The Muon pair masses are: %.3f, %.3f and %.3f GeV/c^2." % (peak_masses[0], peak_masses[1], peak_masses[2]))
    print("The Muon mass differences are: %.3f and %.3f GeV/c^2." %(differences[1], differences[2]))
    mass_ranges, index_ranges = peak_analysis(y_data=n, x_data=bins, peak_index=peak_index)  # peak_location

    peak_region_means = []
    region_var = []
    region_std = []
    std_err = []
    for i in range(len(index_ranges)):
        peak_region_means.append(region_mean(x_data=bins, ind_range=index_ranges[i]))
        region_var.append(region_variance(x_data=bins, ind_range=index_ranges[i]))
        region_std.append(region_stdev(x_data=bins, ind_range=index_ranges[i]))
        # n = index_ranges[i][1] - index_ranges[i][0]
        # std_err.append(std_err_mean(region_std, n))
        # print(peak_region_means[i])
        # print(reigon_var[i])
        # print(reigon_std[i])
    # Still need to find out what std dev on the mean is?! Bias probs because left higher than right
    # print(std_err[0])

    fwhm = FWHM(peak_index[0], index_ranges[0], n, bins)
    sigma = est_sigma(fwhm)
    print("1S peak of: (%.2f +/- %.2f) GeV/c^2." % (peak_masses[0], sigma))


main()

