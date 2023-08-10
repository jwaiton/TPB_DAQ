import numpy as np
import matplotlib.pyplot as plt

'''
    basic script for plotting charge integrals
'''

def main():
    file_path = "output/RUN_31/ADC_data.npy"
    data = np.load(file_path)

    # define your bins here
    bins = 60

    # plot modify to your own liking
    plt.hist(data, bins = bins)    
    plt.xlabel('ADC counts')
    plt.ylabel('Counts')
    plt.show()

main()
