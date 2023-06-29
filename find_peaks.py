import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def main():
    file_path = "output/RUN_17/ADC_data.npy"
    data = np.load(file_path)

    # clip data below 0
    newdata = data[(data>0)]
    bins = 75
    plt.hist(newdata, bins = bins)
    

    counts, bin_edges, _ = plt.hist(newdata, bins = bins)
    
    # alter prominence to alter peak sensitivity
    peaks, _ = find_peaks(counts, prominence = 100)

    plt.plot(bin_edges[peaks], counts[peaks], 'ro')
    plt.yscale('log')

    # adding a bit of flair for report plot
    #plt.title()
    print("Peak values: {}".format(bin_edges[peaks]))
    plt.show()

main()