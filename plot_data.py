import numpy as np
import matplotlib.pyplot as plt

# basic script for plotting data
def main():
    file_path = "output/RUN_12/ADC_data.npy"
    data = np.load(file_path)

    # clip the data
    #newdata = data[(data < 5000)]
    #newerdata = newdata[newdata > -1000]
    bins = 50
    plt.hist(data, bins)
    plt.yscale('log')
    plt.show()

main()
