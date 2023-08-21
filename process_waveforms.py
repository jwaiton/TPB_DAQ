import numpy as np
import matplotlib.pyplot as plt
import plot_data_waveforms
import marc_binning as marcB
from scipy.interpolate import make_interp_spline, BSpline
import pandas as pd

'''
basic script to subtract one waveform from another and then use plot_data_waveforms/chargeint to view these subtracted waveforms
'''


def main():
    # apply at your own leisure here:
    subtract_waveforms(output=True)
    bin_waveforms()
    

def subtract_waveforms(file_path_1 = "output_waveforms/RUN_34/ADC_data.npy", file_path_2 = "output_waveforms/RUN_33/ADC_data.npy", output = False):

    # load data
    data_1 = np.load(file_path_1)
    data_2 = np.load(file_path_2)

    # subtract element-wise
    data_sub = data_1 - data_2
    # option to remove negatives?
    
    # plot new waveform
    plot_data_waveforms.plot_waveform(data = data_sub, time = (100, 99.605))

    if output == True:
        # save new subtracted waveform
        np.save("sub_waveform", data_sub)

    


def bin_waveforms(file_path = "sub_waveform.npy", bin_ratio = 100, time_scale = 100, output = False):
    data_y = np.load(file_path)
    # hard-coded length
    data_x = np.linspace(0,time_scale, num = len(data_y), endpoint = True)
    '''
    no_bins = len(data_x)//bin_ratio
    remainder = len(data_x)%bin_ratio
    # example: moving from 1ns/pt to 100ns/pt. So for 1,000,000 points, have 10,000 new points.
    
    # shrink data_x to the correct size (assume remainder is negligible), as linear in time this works
    shrunk_data_x = np.logspace(np.log10(data_x[0]), np.log10(data_x[-1]), num = (no_bins), endpoint = True)

     # Calculate the logarithmic bin edges
    log_min = np.log10(0.0001)  # Minimum bin edge (adjust as needed)
    log_max = np.log10(len(data_y))  # Maximum bin edge (adjust as needed)
    log_bin_edges = np.logspace(log_min, log_max, num=no_bins + 1)

    shrunk_data_y = []
    for i in range(no_bins):
        start = int(log_bin_edges[i])
        end = min(int(log_bin_edges[i + 1]), len(data_y))
        cumulative = data_y[start:end]
        shrunk_data_y.append(sum(cumulative))   

    plt.plot(log_bin_edges[:-1], shrunk_data_y)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    '''
    '''
    # now integrate around these points respective to the bin ratio
    shrunk_data_y = []
    for i in range(no_bins):
        # take range 0:100, 100:200, etc until reaches full length
        start = i * bin_ratio
        end = min(start + bin_ratio, len(data_y))
        cumulative = data_y[start:end]
        shrunk_data_y.append(sum(cumulative))
    '''
    '''
    # resample/interpolate

    # create x values
    log_x_vals = np.logspace(np.log10(0.001), np.log10(data_x.max()), num = 100)

    y_interp = np.interp(log_x_vals, data_x, data_y)
    print(log_x_vals)
    print(y_interp)
    shrunk_data_y = y_interp

    plt.plot(log_x_vals, y_interp)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    '''

    # create logarithmically separate spaces
    log_x = np.logspace(np.log10(data_x[1]), data_x[-1], num = 20)
    # create pandas dataframe that holds x and y columns for data_x and data_y, cutting off the last 395 time values, and the first 395 amplitude values
    df = pd.DataFrame({'Time':data_x[:-387], 'Amplitude': data_y[387:]})

    # scaling nonsense
    new_min = 10**-6
    new_max = 10

    old_min = df['Amplitude'].min()
    old_max = df['Amplitude'].max()
    scaling_factor = (new_max - new_min) / (old_max - old_min)
    
    df['Amplitude [a.u]'] = (df['Amplitude'] - old_min) * scaling_factor + new_min

    df.plot('Time','Amplitude [a.u]', kind = 'line', legend = False)
    plt.xlim(0.01)
    plt.xlabel('Time [us]', fontsize = 15)
    plt.ylabel('Amplitude [a.u.]', fontsize = 15)
    plt.xscale('log')
    plt.yscale('log')
    plt.xticks(fontsize = 12)
    plt.yticks(fontsize = 12)
    plt.title('Alphas on TPB', fontsize = 22)
    plt.show()
    print(df.head(10))

    if output == True:
        # save binned waveform
        np.save("data_binned_y" + str(time_scale), shrunk_data_y)


    
    plot_data_waveforms.plot_waveform(data = shrunk_data_y, time = (100, 99.6))


    '''
    # log equivalent
    data_x_log = np.logspace(np.log10(0.000562459), np.log10(time_scale), num = len(data_y)//bin_ratio, endpoint = True)
    print(data_x_log)

    # creating binned y array to fill
    data_binned_y = np.zeros(len(data_x_log))

    i = 0
    j = 0

    #print(data_x[10:])
    #print(data_x_log[10:])


    while (i < len(data_x_log)-2):
        # if linspace time array smaller than next step in data_x_log, add to previous bin
        if (data_x_log[i+1] >= data_x[j]):
            data_binned_y[i] += data_y[j]
            j += 1
        else:
            # normalise
            data_binned_y[i] = data_binned_y[i]/j
            # reset at higher i
            j = 0
            i += 1
    
    #print(data_binned_y)

    plt.plot(data_x_log, data_binned_y)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()

    '''


def bin_waveforms_linear(file_path = "sub_waveform.npy", bin_ratio = 2, time_scale = 99.605, output = False):
    '''
    bin linearly the normal waveform
    '''

    data_y = np.load(file_path)
    # hard-coded length
    data_x = np.linspace(0,time_scale, num = len(data_y), endpoint = True)

    ### marcs way, also doesnt work
    #n_bins = marcB.number_of_bins_func(data_x, bin_ratio)
    #hist_val_x, bin_edges_x = np.histogram(data_x, bins=n_bins)
    #bin_centres_x = marcB.get_bin_centers(bin_edges_x)


    #data_y_binned = marcB.binned_data(data_y, n_bins, bin_ratio)


    
    data_binned_x = np.linspace(0, time_scale, num = len(data_y)//bin_ratio, endpoint = True)

    # creating binned y array to fill
    data_binned_y = np.zeros(len(data_binned_x))

    i = 0
    j = 0


    
    while (i < len(data_binned_x)-2):
        # if linspace time array smaller than next step in data_x_log, add to previous bin
        if (data_binned_x[i+1] >= data_x[j]):
            data_binned_y[i] += data_y[j]
            j += 1
        else:
            # normalise
            data_binned_y[i] = data_binned_y[i]/j
            # reset at higher i
            j = 0
            i += 1

    plt.plot(data_binned_x, data_binned_y)
    plt.show()


    plt.plot(data_binned_x, data_binned_y)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    


if __name__ == "__main__":
    main()