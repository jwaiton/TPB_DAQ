import numpy as np
import parse_data
import matplotlib.pyplot as plt


def main(filename = "C1--PMT-test_calibration_long--00000.trc", bin_ratio = 100, debug = False):

    # read data
    data_x, data_y = parse_data.port_event(filename, PATH,x_data = True)
    

    no_bins = len(data_x)//bin_ratio
    remainder = len(data_x)%bin_ratio
    # example: moving from 1ns/pt to 100ns/pt. So for 1,000,000 points, have 10,000 remaining.

    # trim the final samples that don't fit into the division
    data_y = data_y[:-remainder]
    data_x = data_x[:-remainder]

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

    # test
    if debug == True:
        plt.plot(data_x, data_y)
        plt.title("Pre-integration")
        plt.show()
        print("Total value pre-int: {}".format(sum(data_y)))


        plt.plot(shrunk_data_x, shrunk_data_y)
        plt.title("Post-integration")
        plt.show()
        print("Total value post-int: {}".format(sum(shrunk_data_y)))
        



if __name__ == "__main__":

    #PATH = "SR_testing/SR_testing_500NS_5kS/"
    PATH = "calib/calib_1ms_1nspt_HV/"
    test_event = "C1--PMT-test_calibration_long--00000.trc"
    output_dir = "output/"
    main(debug = True)