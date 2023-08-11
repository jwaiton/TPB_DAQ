import numpy as np
import matplotlib.pyplot as plt
import plot_data_waveforms

'''
basic script to subtract one waveform from another and then use plot_data_waveforms/chargeint to view these subtracted waveforms
'''


def main():
    # apply at your own leisure here:
    subtract_waveforms()
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


def bin_waveforms(file_path = "sub_waveform.npy", bin_ratio = 100, time_scale = 99.605, output = False):
    data_y = np.load(file_path)
    # hard-coded length
    data_x = np.linspace(0,time_scale, num = len(data_y), endpoint = True)

    no_bins = len(data_x)//bin_ratio
    remainder = len(data_x)%bin_ratio
    # example: moving from 1ns/pt to 100ns/pt. So for 1,000,000 points, have 10,000 new points.

    # shrink data_x to the correct size (assume remainder is negligible), as linear in time this works
    shrunk_data_x = np.linspace(data_x[0], data_x[-1], num = (no_bins), endpoint = True)

    # now integrate around these points respective to the bin ratio
    shrunk_data_y = []
    for i in range(no_bins):
        # take range 0:100, 100:200, etc until reaches full length
        start = i * bin_ratio
        end = min(start + bin_ratio, len(data_y))
        cumulative = data_y[start:end]
        shrunk_data_y.append(sum(cumulative))
    
    if output == True:
        # save binned waveform
        np.save("binned_y_data_" + str(time_scale), data_y)

    plot_data_waveforms.plot_waveform(data = shrunk_data_y, time = (100, 99.6))

main()