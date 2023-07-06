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
    popt, pcov = curve_fit(combined_func, x, y, p0, maxfev = 500000)
    print(popt, pcov)
    return popt, pcov

def main():
    file_path = "output/RUN_20/ADC_data.npy"
    data = np.load(file_path)

    # clip data below 0
    newdata = data[(data>0)]
    bins = 75
    #plt.hist(newdata, bins = bins)
    
    counts, bin_edges = np.histogram(newdata, bins = bins)

    # guesses for initial parameters (need 7)
    aprio = [550, 0.2, 0.02, 405, 0.034, 781199, 0.0007] # RUN 20 -> 1MS_500NS
    #aprio = [370, 0.05, 0.02, 100, 0.034, 50000, 0.005] # RUN 19 -> 500S_500NS

     # create xspace to plot the function across thats more continuous than the previous binning   
    xspace = np.linspace(0,0.6, len(bin_edges)) # RUN 20 -> 1MS_500NS
    #xspace = np.linspace(0,0.15, len(bin_edges)) # RUN 19 -> 500S_500NS

    # alter prominence to alter peak sensitivity
    peaks, _ = find_peaks(counts, prominence = 100)

    # fit
    bin_centers = bin_edges_to_centers(bin_edges)
    popt, pcov = fit_gauss_2exps(bin_centers, counts, p0 = aprio)
    perr = np.sqrt(np.diag(pcov))

    

    
    # plotting shenanigans
    fig, ax = plt.subplots(figsize = (7,7))

    ax.bar(bin_centers, counts, width=(bin_edges[1] - bin_edges[0]), label=r'Histogram entries')
    ax.plot(xspace, combined_func(xspace, *popt), color='orange', linewidth=2.5, label=r'Fitted function')
    ax.set_xlabel("Arbitrary charge units", fontsize = 15)
    ax.set_ylabel("Entries", fontsize = 15)
    ax.tick_params(axis='x', labelsize = 14)
    ax.tick_params(axis='y', labelsize = 14)


    textstr = '\n'.join((
    r'$A=%.2f$ $\pm~%.3f$' % (popt[0], perr[0], ),
    r'$\mu=%.2f$ $\pm~%.3f$' % (popt[1], perr[1], ),
    r'$\sigma=%.2f$ $\pm~%.3f$' % (popt[2], perr[2], )))

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    # place a text box in upper left in axes coords
    ax.text(0.7, 0.875, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)
    ax.set_yscale("log")
    ax.set_title("Run 20 - 500ns 5kS", fontsize = 17)
    ax.legend()
    #fig.tight_layout()
    plt.show()

    #plt.plot(bin_edges[peaks], counts[peaks], 'ro')
    #plt.yscale('log')

    # adding a bit of flair for report plot
    #plt.title()
    #print("Peak values: {}".format(bin_edges[peaks]))

main()