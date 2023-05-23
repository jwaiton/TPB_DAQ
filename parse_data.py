import lecroyparser as parse
import numpy as np
import matplotlib.pyplot as plt
from os import walk
from os.path import exists
from os import mkdir
from scipy import stats

PATH = "TPC_lab/"
test_event = "C1--PMT-test_calibration_long--12819.trc"
output_dir = "output/"

def plot_signal_event(event_name):
    '''
    plot events that appear to have signal in them (y value much larger than the baseline)
    '''
    data = parse.ScopeData(PATH+str(event_name))

    plt.plot(data.x, data.y)


def port_event(event_name):
    '''
    collect data for a singular lecroy trc file
    '''
    data = parse.ScopeData(PATH+str(event_name))
    #path = PATH+str(event_name)
    #contents = open(path, 'rb').read()
    #data = parse.ScopeData(data=contents)
    return data.y

def port_dir(path):
    '''
    take entire directory of lecroy trc files and move to numpy array
    '''

def display_event():
    '''
    display individual event
    '''


def plot_single():
    '''
    plot single event
    '''
    data = port_event(test_event)
    print(data)
    #plt.plot(data.x, data.y)
    #plt.show()

    return 0

def integrate(y_data):
    '''
    collect the integral across an event by summing y components
    '''
    total = np.sum(y_data)
    return(total)

def ADC_plot(ADCs, bins = 100,run_no = -1):
    '''
    plot charge histogram of event with ADCs along x and events along y
    '''

    # check
    if run_no == -1:
        "Input a run_number before plotting!"
        return

    x_label = "ADC counts"
    y_label = "Counts"
    plt.hist(ADCs, bins)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title("Charge histogram")
    plt.savefig(output_dir + "RUN_" + str(run_no) + "/ADC_plot.png")
    plt.show()

def collate_ADC_data(path_dir):
    '''
    collect all the ADC value across individual events recursively
    '''
    # collect filenames
    filenames = next(walk(path_dir), (None, None, []))[2]
    print("Number of files: {}".format(len(filenames)))

    file_length = len(filenames)
    display_vals = np.linspace(0,file_length, dtype = int, num = 25 )

    ADC_list = []
    for i in range(file_length):
        # integrate y axis of each event and append to ADC_list
        ADC_list += (integrate(subtract_baseline(port_event(filenames[i]),type='mean'))),

        # print when used
        if i in display_vals:
            # print progress
            print("{:.1f}% complete".format((i/len(filenames))*100))

    return ADC_list

def subtract_baseline(y_data, type = 'mean'):
    '''
    remove the pedestal in singular events (quickly!)
    '''


    # convert y_data to numpy array for your own sanity
    y_data = np.array(y_data)

    # MEAN METHOD
    # add all ADC values and divide by length (rough), also remove negatives
    if (type=='mean'):
        total = (np.sum(y_data)/len(y_data))
    # MODE METHOD
    elif (type=='mode'):
        value, counts = np.unique(y_data, return_counts=True)
        m = counts.argmax()
        # counteracting mode being stupid
        #if counts[m] == 1:
        #    print("Only one count of this value, please use a different method! (Mode sucks Brais >:( ))")
        #else:
        #    total = value[m]
        total = value[m]
        ## SCIPY IS SLOW!
        ##return (stats.mode(y_data))
    # MEDIAN METHOD
    elif (type=='median'):
        total = np.median(y_data)
    else:
        print("Please input a baseline method, exiting...")
        return 0

    # return values subtracted
    if (total > 0):
        return y_data - total
    else:
        return y_data - total

def main():

    run_no = input("Run Number: ")

    # make directory if it doesnt exist in output directory
    if exists(output_dir+"RUN_" + str(run_no)):
        print("Directory exists! Overwriting previous data...")
    else:
        mkdir(output_dir+"RUN_" + str(run_no))


    # collect then save data
    data = collate_ADC_data(PATH)
    np.save(output_dir + "RUN_" + str(run_no) + "/ADC_data",np.array(data))


    ## load data
    #data = np.load(output_dir+"RUN_" + str(run_no) + '/ADC_data.npy')

    # hist show data
    ADC_plot(data, bins = 60, run_no = run_no)


    print("Job done!")


main()
