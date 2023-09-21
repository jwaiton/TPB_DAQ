import math as m
import numpy as numpy
from scipy.integrate import quad
from scipy.special import expi
import matplotlib.pyplot as plt
import numpy as np


## CODE FROM MARC SEEMANN
## https://github.com/MarcSeemann/Mphys-Project/blob/Analysis/mc_model.py
## based on V&L model taken from: https://inspirehep.net/literature/1631707


'''
def integrand(t, tau_t, t_a, A):
    return np.exp((-2*t)/tau_t) / (((1 + A*(1*expi((1 * ((t + t_a)/tau_t))) - (1*expi(t_a/tau_t))))**2) * (1+(t/t_a)))

def tau_d_func(tau_t, t_a, A):
    result, _ = quad(integrand, 0, np.inf, args=(tau_t, t_a, A))
    return result

def prompt_func(t, N_p, tau_s):
    return (N_p/tau_s) * np.exp(-t/tau_s)

def slow_func(t, N_d, tau_t, t_a, A):
    F_t = np.exp((-2*t)/tau_t) / (((1 + A*(1*expi((1 * ((t + t_a)/tau_t))) - (1*expi(t_a/tau_t))))**2) * (1+(t/t_a)))
    tau_d = tau_d_func(tau_t, t_a, A)
    # tau_d = 10
    return (N_d/tau_d) * F_t

def V_L_model(t, N_p, tau_s, N_d, A, t_a, tau_t, C):
    return prompt_func(t, N_p, tau_s) + slow_func(t, N_d, tau_t, t_a, A) + C

## 
'''

# DOESNT WORK
def generate_data(t, N_p, tau_s, N_d, A, t_a, tau_t, runs):

    # produce histogram data from function with correct parameters
    # will be using box method ala DAML but better
    # https://github.com/jwaiton/DAML/blob/main/CP4-WAITON-S1739002.ipynb

        # create list of pdf results
    pdf_list = []
        # Take values of t to be upper and lower limits
    l_lim = 0
    h_lim = 1
    t_low = min(t)
    t_high = max(t)
    
    # Find maximal value and multiply to be above distribution by minor amount
    f_max = VL_fit(0.01, N_p, tau_s, N_d, A, t_a, tau_t, C)*1.1
    print('Generating data...')
    i = 0

    while(len(pdf_list) < runs):

        # counting
        if (i %2000 == 0):
            print("Loop: {}\nData: {}".format(i, len(pdf_list)))
        elif ((len(pdf_list) != 0) and ( i // len(pdf_list) > 1000)):
            print("Lots of loops with little data, are you sure you've processed it correctly?")
        
            # generation random number within pdf range scale between upper and lower limits
            # needs to be exponent for logarithmic normalisation
        x1 = loguniform.rvs(1e-2, 1e0, size = 1)
        x1 = t_low + (t_high - t_low)*x1
            # apply to the pdf
        y1 = VL_fit(x1, N_p, tau_s, N_d, A, t_a, tau_t, C)
            # generate second random number between our range
        y2 = loguniform.rvs(1e-2, 1e0, size = 1)
        y2 = f_max*y2

        # counting
        i += 1

            # if y2 < y1 add to list
        if (y2 < y1):
            pdf_list.append(x1)
        else:
            continue;
    
    return pdf_list

# DOESNT WORK
def generate_MC(t, N_p, tau_s, N_d, A, t_a, tau_t, runs):
    
    vals = []

    for i in range(runs):
        print(i)
        ar = np.zeros(runs)

        for i in range(len(ar)):
            ar[i] = np.random.uniform(low = min(t), high = max(t))

        integral = 0.0

        for i in ar:
            integral += VL_fit(i, N_p, tau_s, N_d, A, t_a, tau_t, C)

        soln = (max(t) - min(t))/float(runs)*integral
        
        vals.append(soln)

    return vals



## Re-imagined to be less impossible to read

def Ft(t, tau_t, t_a, A):
    # Function F_t
    numer = np.exp((-2*t)/(tau_t))

    exp_int_comp = (expi(-(t+t_a/tau_t)) - expi(-(t_a/tau_t)))
    deno = np.square(1 + A * (exp_int_comp)) * (1 + t/t_a)

    F_t = numer/deno

    return F_t

def prompt_comp(t, N_p, tau_s):
    return (N_p/tau_s) * np.exp(-t/tau_s)

def slow_comp(t, N_d, tau_t, t_a, A):
    
    F_t = Ft(t, tau_t, t_a, A)

    # integral over F_t 
    tau_d, _ = quad(Ft, 0, np.inf, args=(tau_t, t_a, A))
    
    return (N_d/tau_d) * F_t


def VL_fit(t, N_p, tau_s, N_d, A, t_a, tau_t, C):
    return (((prompt_comp(t, N_p, tau_s) + slow_comp(t, N_d, tau_t, t_a, A))) + C)



def generate_fake_data(t, N_p, tau_s, N_d, A, t_a, tau_t):

    # setting constant to zero as histogram application raises values enough to apply the expected C height.
    C = 0
    sampling_size = 1000000

    # generate default values
    y_vals = VL_fit(t, N_p, tau_s, N_d, A, t_a, tau_t, C)

    # use two log spaces to ensure adequate values around low t
    t1 = np.logspace(-2, 1, 1000)
    t2 = np.logspace(0.5, 3, 1000)

    # produce VL_fit across all data values
    y_1 = VL_fit(t1, N_p, tau_s, N_d, A, t_a, tau_t, C)
    y_2 = VL_fit(t2, N_p, tau_s, N_d, A, t_a, tau_t, C)

    # collect random samples from the VL_fit
    sample_1 = np.random.choice(t1, size = sampling_size, p=y_1/sum(y_1)) 
    sample_2 = np.random.choice(t2, size = sampling_size, p=y_2/sum(y_2)) 

    # create smaller binning across same logspace for the sampled 
    bin_widths_1 = np.logspace(-2, 1, 51)
    bin_widths_2 = np.logspace(0.5, 3, 51)

    # produce histograms
    ny_1, nx_1 = np.histogram(sample_1, bins=bin_widths_1)
    ny_2, nx_2 = np.histogram(sample_2, bins=bin_widths_2)

    # alter bin edges to bin centers
    nx_1 = nx_1[:-1]+np.diff(nx_1)/2
    nx_2 = nx_2[:-1]+np.diff(nx_2)/2

    print(ny_1[:-8])
    print("============")
    print(ny_2)

    # combine both spaces (remove last 8 samples)
    comb_x = np.concatenate([nx_1[:-8], nx_2])
    comb_y = np.concatenate([ny_1[:-8], ny_2/25]) # ny_2/535 #for some reason? 25 seems to work better?
    # produce error
    comb_e = (((comb_y*100)**0.5/100)**2+1/sampling_size)**0.5 # poisson error + monte carlo
    #print(new_x_1)
    #print("=======")
    #print(new_x_2)
    # return 'simulated values'
    plt.errorbar(comb_x, comb_y/50000, yerr=comb_e/50000, label=r'Monte Carlo Data', alpha=0.5) # the 50000 plotting is just for overlaying the MC and model
    plt.plot(t, y_vals, label = r'V&L Model')
    plt.xscale('log')
    plt.yscale('log')
    plt.ylim([10**(-7),100])
    plt.xlim([10**(-2),1000])
    plt.legend(fontsize = '10')

    plt.show()

    return comb_x, comb_y, comb_e




def produce_toy(N_p, tau_s, N_d, A, t_a, tau_t, type, debug = False, plot = False):

    # time scale across 0 -> 1ms.
    # 0 -> 3 in log space is 0 -> 1000 us, the scale we want.
    t = np.logspace(-2, 3, 100000)
    if debug == True:
        y = np.zeros(100)
        plt.plot(t, y, 'o')
        #plt.xscale('log')
        plt.show()

    if plot == True:
        C = 0 # set C to zero here
        y_vals = VL_fit(t, N_p, tau_s, N_d, A, t_a, tau_t, C)
        plt.plot(t, y_vals)
        plt.title(type)
        plt.xlabel('Time (us)')
        plt.ylabel('Arbitary Amplitude')
        plt.xscale('log')
        plt.yscale('log')
        plt.show()

    # generate data
    
    return generate_fake_data(t, N_p, tau_s, N_d, A, t_a, tau_t)
    #pdf_list = generate_MC(t, N_p, tau_s, N_d, A, t_a, tau_t, runs = 1000)
    #print("Done generating")
    #np.save('sim_data_VL', pdf_list)
    #plt.hist(pdf_list, bins = 100)
    #plt.show()

def fit_toy(x_mc, y_mc, e_mc, fit_args):
    # put fit here
    x = 0

def plot_simdata(filename):

    # load in saved data
    pdf_list = np.load(filename)

    plt.hist(pdf_list, bins = np.logspace(-2, 3, 50))
    plt.xscale('log')
    plt.show()

def main():

    # parameters to tune
    betas295k  = {'N_p': 0.74, 'tau_s': 4.6, 'N_d': 0.26, 'A': 0.19, 't_a': 0.095, 'tau_t': 350, 'type': "betas@295K"}
    alphas295k = {'N_p': 0.21, 'tau_s': 5.6, 'N_d': 0.79, 'A': 0, 't_a': 0.08, 'tau_t': 200, 'type': "alphas@295K"}
    photonsAr  = {'N_p': 0.89, 'tau_s': 8.3, 'N_d': 0.11, 'A': 0.9, 't_a': 0.2, 'tau_t': 160, 'type': "128nm Photons"}

    # produce the fake data using VL fit + parameters
    x_mc, y_mc, e_mc = produce_toy(**betas295k)

    fit_toy(x_mc, y_mc, e_mc, fit_args)

    #plot_simdata('sim_data_VL.npy')

    # apply fit to toy data
    #VL_fit()

if __name__ == "__main__":
    main()
