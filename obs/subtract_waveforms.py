import numpy as np
import matplotlib.pyplot as plt
import plot_data_waveforms

'''
basic script to subtract one waveform from another and then use plot_data_waveforms/chargeint to view these subtracted waveforms
'''


def main():
    


    # Initial file path
    file_path_1 = "output_waveforms/RUN_32/ADC_data.npy"
    # Subtraction file path
    file_path_2 = "output_waveforms/RUN_33/ADC_data.npy"

    # load data
    data_1 = np.load(file_path_1)
    data_2 = np.load(file_path_2)

    # subtract element-wise
    data_sub = data_1 - data_2
    # option to remove negatives?
    
    # plot new waveform
    plot_data_waveforms.plot_waveform(data = data_sub)


main()