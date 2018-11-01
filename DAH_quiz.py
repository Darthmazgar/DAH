import matplotlib.pyplot as plt
import numpy as np


def get_norm_numbers(mu, sigma, number):
    """
    Generate a list of random numbers based around a normal distribution
    with params, mu and sigma.
    """
    return np.random.normal(mu, sigma, number)


def plot_hist(data, bins=150, title="", x_lab="", y_lab="", save=False, show=True):
    plt.hist(data, bins)
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.title(title)
    if save:
        plt.savefig(save)
    if show:
        plt.show()


def main():
    mu = 3  # Define parameters.
    sigma = 2

    s = get_norm_numbers(mu, sigma, 1000000)

    bins = 150
    bin_size = (np.max(s) - np.min(s))/ bins

    plot_hist(s, bins=bins, title="Normal Distribution Generated from Random Numbers\n$\sigma=%.1f$;  $\mu=%.1f$" % (sigma, mu),
              x_lab="x Value", y_lab="Frequency [%.4f/bin]" % bin_size, save="normal2.jpg")

    mean = np.mean(s)  # Calculate statistics about data.
    var = np.var(s)

    print("Mean: %.3f; Variance: %.3f" % (mean, var))

main()






