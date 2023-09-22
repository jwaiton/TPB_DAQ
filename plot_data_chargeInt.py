import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
'''
    basic script for plotting charge integrals
'''

def gauss_1(x, amp, mu, dev, C):
    g_1 = amp*np.exp(-(x - mu)** 2 / (2 * dev ** 2)) + C
    return g_1

# gaussian function for fitting
def gauss_2(x, amp_1, mu_1, dev_1, C_1, amp_2, mu_2, dev_2, amp_3, edec_1):
    '''
    Gaussian Function
    '''

    g_1 = amp_1*np.exp(-(x - mu_1)** 2 / (2 * dev_1 ** 2))

    g_2 = amp_2*np.exp(-(x - mu_2)** 2 / (2 * dev_2 ** 2))

    e_1 = amp_3 * np.exp(-x / edec_1)

    return ((C_1 + ( g_1 ) + ( g_2 ))) #+ ( e_1 )))


def exp(x, amp, scale, pos):
    '''
    Exponential Function
    '''
    return amp*np.exp(pos - (x/scale))

def fit_gaussians(data, bin_no = 100, gauss_n = 1):
    '''
    Fit N gaussians to charge integral data from histogram.
    '''
    # prominence of peak and valleys, set to 100 to remove noise
    prom = 100

    # take histogram values
    heights, bin_pos = np.histogram(data, bins = bin_no)

    # take bin centres
    bin_pos = bin_pos[:-1]+np.diff(bin_pos)/2
    '''
    plt.plot(bin_pos, heights)
    plt.show()
    '''
    # continue searching for peaks and valleys until you have 2 peaks, 1 valley
    while True:

        # find valley
        valleys, _ = find_peaks(-heights, prominence = prom)

        # find peaks
        peaks, _ = find_peaks(heights, prominence = prom)

        if ((len(peaks) == 2) and (len(valleys) == 1)):
            break
        # not enough peaks, decrease prominence
        elif ((len(peaks) < 2) and (len(valleys) == 0)):
            # increase prominence incrementally. This will almost 100% break
            prom = 0.9*prom
        else:
            prom = 1.1*prom

    '''
    # PLOT THIS WITH BIN_POS PROPERLY
    plt.plot(peaks, heights[peaks], 'xr', label=r'Peaks'); 
    plt.plot(valleys, heights[valleys], 'xb', label=r'Valleys'); 
    plt.plot(heights); 
    plt.yscale('log'); 
    plt.show()

    plt.plot(bin_pos[peaks], heights[peaks], 'xr')
    plt.plot(bin_pos, heights);
    plt.title("testing")
    plt.show()
    '''
    print("Peaks")
    print(peaks)

    print(heights[peaks])
    print(bin_pos[peaks][1])

    peak_height = heights[peaks][0]
    valley_height = heights[valleys][0]

    # fit gaussian
    # first peak fitting

    # take gap between peak and valley
    p_v_t_gap = peaks[1] - valleys[0]
    # take mask across x values over which we'll fit two gaussians.
    



    #####################################

    ############   FITTING WITH ONE GAUSSIAN

    #####################################

    if (gauss_n == 1):
        
        # initial guesses
        ampg = 3500
        mug = bin_pos[peaks[1]]
        devg = 0.0001
        Cg = 100

        x = bin_pos[valleys[0]:valleys[0]+(p_v_t_gap*2)+1] # fine tuned
        y = heights[valleys[0]:valleys[0]+(p_v_t_gap*2)+1]

        plt.plot(x,y)
        plt.title('Range of fitting for singular gaussian')
        plt.show()

        popt, pcov = curve_fit(lambda bin_pos, amp, mu, dev, C: gauss_1(x, amp, mu, dev, C), x, y, 
                            maxfev = 50000000, 
                            p0 = np.array([ampg, mug, devg, Cg]),
                            #              amp_1 dev_1   C_1  amp_2 dev_2 amp_3 edec_1
                            bounds = (-1E5, 1E5)
                            ) 

        plt.plot(x,y)
        plt.title('Singular Gaussian Fit')
        plt.plot(x, gauss_1(x, popt[0], popt[1], popt[2], popt[3]))
        plt.show()

    #####################################

    ############   FITTING WITH TWO GAUSSIANS

    #####################################
    if (gauss_n == 2):


        x = bin_pos[valleys[0]:valleys[0]+(p_v_t_gap*4)]
        y = heights[valleys[0]:valleys[0]+(p_v_t_gap*4)]

        plt.plot(x,y)
        plt.title('Range of fitting for two gaussians')
        plt.show()

        # take first peak to be mu
        f_mu = bin_pos[peaks][1]
        print("f_mu")
        print(f_mu)

        #initial guesses
        amp1    = 3500; 
        mu1     = bin_pos[peaks][1]; 
        dev1    = 0.001;
        C1      = 100;
        amp2    = 555;
        mu2     = mu1*2;
        dev2    = 0.001;
        amp3    = 1;
        edec1   = 1;
        ''' # MU FIXED
        popt, pcov = curve_fit(lambda bin_pos, amp_1, dev_1, C_1, amp_2, dev_2, amp_3, edec_1: gauss_2(x, amp_1, f_mu, dev_1, C_1, amp_2, f_mu*2, dev_2, amp_3, edec_1), x, y, 
                            maxfev = 50000000, 
                            p0 = np.array([3500, 0.0149, 1020, 600, 0.03, 1, 1]),
                            #              amp_1 dev_1   C_1  amp_2 dev_2 amp_3 edec_1
                            bounds = (-1E5, 1E5)
                            ) 
        '''
        # MU NOT FIXED
        popt, pcov = curve_fit(lambda bin_pos, amp_1, mu_1, dev_1, C_1, amp_2, mu_2, dev_2, amp_3, edec_1: gauss_2(x, amp_1, mu_1, dev_1, C_1, amp_2, mu_2, dev_2, amp_3, edec_1), x, y, 
                            maxfev = 50000000, 
                            p0 = np.array([amp1, mu1, dev1, C1, amp2, mu2, dev2, amp3, edec1]),
                            #              amp_1 dev_1   C_1  amp_2 dev_2 amp_3 edec_1
                            bounds = (-1E5, 1E5)
                            ) 
        print(popt)
        # amp, mu, dec, C
        #initial_params = [heights[peaks][1], bin_pos[peaks[1]], .02, heights[valleys][0]]
        #print(initial_params)
        #popt, pcov = curve_fit(gauss, bin_pos[valleys[0]], heights, bounds = ((0, bin_pos[peaks[1]]*0.99, 0.005, 1000), (heights[peaks[0]]*2, bin_pos[peaks[1]]*1.01, 0.05, np.inf)))
        #print(popt, pcov)
        '''
        plt.plot(x,y)
        plt.plot(x, gauss_2(x, popt[0], f_mu, popt[1], popt[2], popt[3], f_mu*2, popt[4], popt[5], popt[6]))
        plt.show()

        #plt.plot(bin_pos, gauss(bin_pos, 3530, 11, 0.014, 1501))
        plt.plot(bin_pos, heights)
        plt.plot(bin_pos, gauss_2(bin_pos, popt[0], f_mu, popt[1], popt[2], popt[3], f_mu*2, popt[4], popt[5], popt[6]))
        plt.yscale('log')
        plt.show()
        '''
        plt.plot(x,y)
        plt.title('Two Gaussian Fit')
        plt.plot(x, gauss_2(x, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7], popt[8]))
        plt.show()


def main():
    file_path = "output/RUN_38/ADC_data.npy"
    data = np.load(file_path)

    # define your bins here
    bins = 200

    # plot modify to your own liking
    plt.hist(data, bins = bins)    
    plt.xlabel('ADC counts')
    plt.ylabel('Counts')
    plt.yscale('log')
    plt.show()


    fit_gaussians(data)
main()
