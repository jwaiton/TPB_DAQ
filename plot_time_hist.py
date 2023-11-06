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
PATH = "../../../../../media/e78368jw/T7/33_3mV_PMT1003_meantime/"
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
    print(filenames[-1])
    print("Number of files: {}".format(len(filenames)))

    # APPLY THIS!!!
    # https://stackoverflow.com/questions/47850202/plotting-a-histogram-on-a-log-scale-with-matplotlib

    data = parse.ScopeData(PATH+str(filenames[-1])).y
    plt.subplot(211)
    plt.ylabel('Counts')
    hist, bins, _ = plt.hist(data, bins = 100)
    logbins = np.logspace(np.log10(bins[0]), np.log10(bins[-1]), len(bins))
    plt.subplot(212)
    plt.hist(data, bins=logbins)
    plt.xscale('log')

    plt.xlabel('Time (s)')
    plt.ylabel('Counts')
    plt.show()

main()
