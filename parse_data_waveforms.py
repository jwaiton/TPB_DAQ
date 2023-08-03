import lecroyparser as parse
import numpy as np
import matplotlib.pyplot as plt
from os import walk
from os.path import exists
from os import mkdir
from scipy import stats

# IMPROVE THIS BY MAKING A SEPARATE 'FUNCTIONS' PY
import parse_data

'''
Script that creates basic waveform plot
'''


def main():

    ### FILE FORMATTING ###

    # defaults

    # make it run fast or not (remove stdev component and just add waveforms normally)
    fast_running = True

    PATH = "alpha_test/alpha_vac_1nsppt/"     # file directory
    file_format = 'C1--PMT-test_calibration_long--' #00000.trc    file
    output_dir = "output_waveforms/"    # output directory

    run_no = input("Run Number: ")

    # make directory if it doesnt exist in output directory
    if exists(output_dir+"RUN_" + str(run_no)):
        print("Directory exists! Overwriting previous data...")
    else:
        mkdir(output_dir+"RUN_" + str(run_no))


    ### DATA COLLECTION AND PROCESSING ###

    filenames = next(walk(PATH), (None, None, []))[2]
    print("Number of files: {}".format(len(filenames)))


    # collect number of files
    file_length = len(filenames)
    display_vals = np.linspace(0,file_length, dtype = int, num = 25 )
    # create array thats length of singular event. 

    # hard coded as we have 1mil sample events, 
    # change the array size just because the operations rely on having a bit of 'extra room'
    # as not all events have the same number of samples (1mil+1, 1mil+2, 1mil+3...)
    if (fast_running == False):
        waveform_array = np.zeros(1000003)    
    else:
        waveform_array = np.zeros(1000001)

    # scan across all files
    for i in range(file_length):

        # collect event
        data_x, a = parse_data.port_event(filenames[i], PATH, x_data = True)
        # flip
        a = -a

        # subtract baseline
        b = parse_data.subtract_baseline(a, type = 'median')

        if (fast_running == False):
            # find std and scan files to see if any are above this.
            stdev = np.std(b)

            for j in range(len(b)):
                # if data in the file is above standard deviation and positive
                if (b[j] > stdev) and (b[j] > 0):
                    # add to specific element in the waveform array
                    waveform_array[j] += b[j]
        else:
            # make b positive
            # add waveform array normally if you are in a rush, setting in defaults
            waveform_array += np.abs(b[0:len(waveform_array)])

        # print when used
        if i in display_vals:
            # print progress
            print("{:.1f}% complete".format((i/len(filenames))*100))

    
    # normalise waveform array DONT CURRENTLY
    #waveform_norm = np.divide(waveform_array, file_length)
    np.save(output_dir + "RUN_" + str(run_no) + "/ADC_data",np.array(waveform_array))

    # plot waveform_norm along y with X being time
    plt.plot(np.linspace(0,len(waveform_array),num = len(waveform_array),endpoint = True), waveform_array)
    plt.yscale('log')
    plt.show()



main()


