import lecroyparser as parse
import numpy as np
import matplotlib.pyplot as plt
from os import walk
from os.path import exists
from os import mkdir
from scipy import stats

import core.plotting as pl
'''
    John Waiton - 2023
        Plots TRC files continuously from PATH
'''


#PATH = "TPC_lab/"
PATH = "../../../../../media/e78368jw/SAMSUNG/tpblab/alpha_150mV_trig/"
test_event = "C1--PMT-test_calibration_long--00000.trc"
output_dir = "output/"


def main():
    filenames = next(walk(PATH), (None, None, []))[2]
    print(filenames[1])
    print("Number of files: {}".format(len(filenames)))

    for i in range(len(filenames)):
        pl.plot_signal_event(filenames[i], PATH)


main()
