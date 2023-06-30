import lecroyparser as parse
import numpy as np
import matplotlib.pyplot as plt
from os import walk
from os.path import exists
from os import mkdir
from scipy import stats

'''
Simple plotting script
'''


#PATH = "TPC_lab/"
PATH = "SR_testing/SR_testing_500NS_1MS/"
test_event = "C1--PMT-test_calibration_long--00000.trc"
output_dir = "output/"

def plot_signal_event(event_name):
    '''
    plot events that appear to have signal in them (y value much larger than the baseline)
    '''
    data = parse.ScopeData(PATH+str(event_name))
    x_vals = np.linspace(0,len(data.x), dtype = int, num = len(data.x), endpoint = True)
    #plt.plot(data.x, data.y)
    print(len(data.x))
    plt.plot(x_vals, -data.y)
    plt.title(str(event_name))
    plt.show()



def main():
    filenames = next(walk(PATH), (None, None, []))[2]
    print(filenames[1])
    print("Number of files: {}".format(len(filenames)))

    for i in range(len(filenames)):
        plot_signal_event(filenames[i])


main()
