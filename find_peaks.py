import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

def bin_edges_to_centers(bin_edges):
    # Calculate the bin widths
    bin_widths = np.diff(bin_edges)
    
    # Calculate the central bin values
    bin_centers = bin_edges[:-1] + bin_widths / 2
    
    return bin_centers

def combined_func(x, amplitude_gaussian, mean_gaussian, sigma_gaussian,amplitude_exp1, decay_exp1,amplitude_exp2, decay_exp2):
    return (amplitude_gaussian * np.exp(-((x - mean_gaussian) ** 2) / (2 * (sigma_gaussian ** 2))) + amplitude_exp1 * np.exp(-x / decay_exp1) 
            + amplitude_exp2 * np.exp(-x / decay_exp2))

def fit_gauss_2exps(x, y, p0):
    popt, pcov = curve_fit(combined_func, x, y, p0, maxfev = 50000)
    print(popt, pcov)
    return popt, pcov

def main():
    file_path = "output/RUN_17/ADC_data.npy"
    data = np.load(file_path)

    # clip data below 0
    newdata = data[(data>0)]
    bins = 75
    #plt.hist(newdata, bins = bins)
    

    counts, bin_edges = np.histogram(newdata, bins = bins)
    
    # alter prominence to alter peak sensitivity
    peaks, _ = find_peaks(counts, prominence = 100)

    # fit
    bin_centers = bin_edges_to_centers(bin_edges)
    aprio = [0.05, 0.002, 0.0005, 0.1, 0.1463, 0.1, 0.147] # guesses for initial parameters (need 7)
    popt, pcov = fit_gauss_2exps(bin_centers, counts, p0 = aprio)
    perr = np.sqrt(np.diag(pcov))

    # create xspace to plot the function across thats more continuous than the previous binning
    xspace = np.linspace(0,0.15, len(bin_edges)) # need to tune stop value by hand
    
    # plotting shenanigans
    fig, ax = plt.subplots()

    ax.bar(bin_centers, counts, width=(bin_edges[1] - bin_edges[0]), label=r'Histogram entries')
    ax.plot(xspace, combined_func(xspace, *popt), color='orange', linewidth=2.5, label=r'Fitted function')
    ax.set_xlabel("Vns", fontsize = 15)
    ax.set_ylabel("Entries", fontsize = 15)


    textstr = '\n'.join((
    r'$A=%.2f$ $\pm~%.3f$' % (popt[0], perr[0], ),
    r'$\mu=%.2f$ $\pm~%.3f$' % (popt[1], perr[1], ),
    r'$\sigma=%.2f$ $\pm~%.3f$' % (popt[2], perr[2], )))

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    # place a text box in upper left in axes coords
    ax.text(0.65, 0.8, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)
    ax.set_yscale("log")
    ax.set_title("Run 17")
    ax.legend()
    plt.show()

    #plt.plot(bin_edges[peaks], counts[peaks], 'ro')
    #plt.yscale('log')

    # adding a bit of flair for report plot
    #plt.title()
    #print("Peak values: {}".format(bin_edges[peaks]))

main()