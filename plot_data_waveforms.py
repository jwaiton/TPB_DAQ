import numpy as np
import matplotlib.pyplot as plt

'''
    basic script for plotting waveforms
'''

def plot_waveform(file_path = 'NA', data = 'NA', time = (100,90)):
    if (file_path != 'NA'):
        new_data = np.load(file_path)
        print("Processing {}".format(file_path))
    elif (data != 'NA'):
        print("Processing data...")
        new_data = data
    else:
        print("Please provide input")
    
    #data = np.load(file_path)

    print(len(new_data))
    # figure out how much data to strip
    div_frac = (time[1]/time[0])
    # then strip it!
    strip_val = len(new_data) - int(len(new_data)*div_frac)
    new_data = new_data[strip_val:]
    print(len(new_data))
    #newerdata = newdata[newdata > -1000]
    #newdata = data[(data>0)]
    bins = 100
    #plt.hist(newdata, bins)

    # subtract median
    new_data = np.abs(new_data - np.median(new_data))

    # CURRENT SETUP FOR PRODUCING WAVEFORM PLOTS ACROSS X TIMESCALE, set range to 0,1000 for 1ms.
    plt.plot(np.linspace(0,99.605,num = len(new_data),endpoint = True),new_data)
    
    plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Time [us]')
    plt.ylabel('Amplitude [a.u.]')
    plt.show()

if __name__ == "__main__":
    file_path = "output_waveforms/RUN_34/ADC_data.npy"
    plot_waveform(file_path = file_path)
