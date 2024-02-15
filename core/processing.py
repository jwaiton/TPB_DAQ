import lecroyparser as parse
import numpy as np
import matplotlib.pyplot as plt
from os import walk
from os.path import exists
from os import mkdir
from scipy import stats

# all functions required to process the relevant data

def port_event(event_name, PATH, x_data = False):
    '''
    collect data for a singular lecroy trc file
    '''
    data = parse.ScopeData(PATH+str(event_name))
    #path = PATH+str(event_name)
    #contents = open(path, 'rb').read()
    #data = parse.ScopeData(data=contents)
    ####print("Initial data value: {}".format(data.y[25]))
    if (x_data == False):
        return data.y
    elif (x_data == True):
        return data.x, data.y



def integrate(y_data):
    '''
    collect the integral across an event by summing y components
    '''
    ####print("Baseline subtracted value: {}".format(y_data[25]))
    int_tot = np.sum(y_data)
    return(int_tot)



def integrate_range(y_data, window = 0, debug = False):
    '''
    Selects range to integrate over based on largest value within the event. 
    If no window is given, chooses 10.

    Perhaps make 'central value' choice an option later rather than largest value? undecided
    '''
        # if window != 0, find index of largest event in data
    if (window == 0 ):
        window = 10
        

    # find largest event
    peak_index = np.argmax(y_data)
    y_max = y_data[peak_index] # fixing issue with debug counting

    # safety check to make sure index overflow doesn't occur
    # if overflow, set window to centre
    if ((peak_index-window) < 0)  or (peak_index+window > len(y_data)):
        if debug == True:
            print("Window overlapping with array edges, setting to centre...")

        peak_index = len(y_data)//2
    # take samples around this relating to the window and save them for integration
    y_data = y_data[peak_index-window:peak_index+window]
    
    if debug == True:
        print("Max value {:.4g} found at index {:.4g}. Integrating...".format(y_max, peak_index))

    return(integrate(y_data))



def collate_ADC_data(PATH):
    '''
    collect all the ADC value across individual events recursively
    '''
    # collect filenames
    filenames = next(walk(PATH), (None, None, []))[2]
    print(filenames[1])
    print("Number of files: {}".format(len(filenames)))

    file_length = len(filenames)
    plot_numbers = np.linspace(0,2000002, dtype = int, num = 2000002, endpoint = True)
    display_vals = np.linspace(0,file_length, dtype = int, num = 25 )

    ADC_list = []
    for i in range(file_length):
        # integrate y axis of each event and append to ADC_list

        # breaking it down into constituent components for testing
        #plot_signal_event("C1--PMT-test_calibration_long--01934.trc")
        #print(filenames[i])
        try:
            a = port_event(filenames[i], PATH)
            # flip to positive
            a = -a
            #print(a)

            b = subtract_baseline(a, type = 'median')
            #print(b)
            c = integrate_range(b, window = 10, debug=False)
            #if (c < -500):
            #    print(c)
            #    plt.plot(plot_numbers,a)
            #    plt.show()

            ADC_list += (c),

            # print when used
            if i in display_vals:
                # print progress
                print("{:.1f}% complete".format((i/len(filenames))*100))


        except Exception as e:
            print(e)
            pass
    return ADC_list

def subtract_baseline(y_data, type = 'median'):
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
    return y_data - total


### Example usage

def main():

    #plot_signal_event(test_event)

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

if __name__ == "__main__":

    #PATH = "SR_testing/SR_testing_500NS_5kS/"
    PATH = "alpha_test_100us/56mV_trig_100us_dark8hrs/"
    test_event = "C1--PMT-test_calibration_long--00000.trc"
    output_dir = "output/"
    main()
