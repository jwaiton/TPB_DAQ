import numpy as np
import matplotlib.pyplot as plt

# basic script for plotting data
def main():
    file_path = "output/RUN_15/ADC_data.npy"
    data = np.load(file_path)

    # clip the data
    #newdata = data[(data < 5000)]
    #newerdata = newdata[newdata > -1000]
    newdata = data[(data>0)]
    bins = 100
    plt.hist(newdata, bins)
    #plt.yscale('log')
    plt.show()

main()
