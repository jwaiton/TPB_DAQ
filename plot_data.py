import numpy as np
import matplotlib.pyplot as plt

# basic script for plotting data
def main():
    file_path = "output_waveforms/RUN_4/ADC_data.npy"
    data = np.load(file_path)

    # clip the data
    #newdata = data[(data < 5000)]
    #newerdata = newdata[newdata > -1000]
    #newdata = data[(data>0)]
    bins = 100
    #plt.hist(newdata, bins)

    # CURRENT SETUP FOR PRODUCING WAVEFORM PLOTS ACROSS 1ms TIMESCALE
    plt.plot(np.linspace(0,1000,num = len(data),endpoint = True),data)
    
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Time [us]')
    plt.ylabel('Amplitude [a.u.]')
    plt.show()

main()
