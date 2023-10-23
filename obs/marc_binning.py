#import lecroyparser
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#import boost_histogram as bh
from matplotlib import colors
#import csv
#import time
#import os


# Functions lifted from Marc

def bin_pos_func(x_min, x_max, n_bins, p_per_bin):
    bin_width = p_per_bin * 2
    bin_loc_arr = np.linspace(x_min + bin_width / 2, x_max - bin_width / 2, n_bins)
    return bin_loc_arr

def number_of_bins_func(x, p_per_bin):
    return (len(x) - len(x) % p_per_bin) // p_per_bin

def get_points_per_bin(num_bins, num_points):
    points_per_bin = num_points // num_bins
    remainder = num_points % num_bins
    if remainder > 0:
        points_per_bin += 1
    return points_per_bin


def binned_data(y, n_bins, p_per_bin):
    y = y[:n_bins * p_per_bin]
    return np.sum(y.reshape(-1, p_per_bin), axis=1)


def get_bin_centers(bin_edges):
    # calculate the bin widths
    bin_widths = np.diff(bin_edges)

    # calculate the bin centers
    bin_centers = bin_edges[:-1] + bin_widths / 2

    return bin_centers