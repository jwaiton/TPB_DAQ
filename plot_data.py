import numpy as np
import matplotlib.pyplot as plt

# basic script for plotting data
def main():
    file_path = "output/RUN_11/ADC_data.npy"
    data = np.load(file_path)

    # clip the data
    newdata = data[(data < 5000)]
    newerdata = newdata[newdata > -1000]
    bins = 50
    plt.hist(newerdata, bins)
    plt.yscale('log')
    plt.show()

main()
