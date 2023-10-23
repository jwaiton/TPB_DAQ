'''
John Waiton - 25.09.2023
    Script that outputs plot and ADC score for any TRC file passed to it.
    Assumes file structure matches expected 'C1--PMT-test_calibration_long--' format.

'''

import lecroyparser as parse
import numpy as np
import matplotlib.pyplot as plt
from os import walk
from os.path import exists
from os import mkdir
from scipy import stats


import core.processing as proc
import core.plotting   as pl


def main():
    # defaults
    PATH = "calib/"     # file directory
    file_format = 'C1--PMT-test_calibration_long--' #00000.trc    file
    output_dir = "analyse_trc_output/"    # output directory

    # collect file name
    file_no = input("File Number: ")
    # generate file name
    file_name = file_format+ str(file_no) + ".trc"

    # make directory if it doesnt exist in output directory
    if exists(output_dir+"FILE_" + str(file_no) + "/"):
        print("Directory exists! Overwriting previous data...")
    else:
        mkdir(output_dir+"FILE_" + str(file_no) + "/")

    data = proc.port_event(file_name, PATH)

    try:
        # collect data
        
        
        # subtract baseline
        sub_data = proc.subtract_baseline(data, type = 'median')

        # integrate
        int_val = -proc.integrate(sub_data)

        print("Integrated value: {:.5g}".format(int_val))

        # plot data
        pl.plot_signal_event(file_name, PATH)
    except:
        print("File within {} not found!".format(file_name))
        pass

main()