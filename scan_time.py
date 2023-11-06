'''
    Script that scans across the timestamps of all files given and produces a binned histogram across time for their creations
'''


import time
import os
from datetime import datetime
import numpy as np
import pandas as pd
from os import walk
import matplotlib.pyplot as plt


def main():
    # generate file paths
    file_path = "../../../../../media/e78368jw/T7/33_3mV_box_in_box_0510_2023/"
    test_event = "C1-----00000.trc"

    file_stat = os.stat(file_path+test_event)
    c_time = file_stat.st_ctime
    creation_time = datetime.fromtimestamp(c_time)
    print(creation_time)

    date1 = pd.Timestamp(creation_time)

    filenames = next(walk(file_path), (None, None, []))[2]
    file_length = len(filenames)


    dates = []

    for i in range(file_length):
        file_stat = os.stat(file_path+filenames[i])
        c_time = file_stat.st_ctime
        creation_time = datetime.fromtimestamp(c_time)
        timestamp = pd.Timestamp(creation_time)
        dates.append(timestamp)
    
    df = pd.DataFrame({'dates': dates})
    # split dataframe between days
    df_27 = df.loc[df['dates'].dt.day == 5]
    df_28 = df.loc[df['dates'].dt.day == 6]
    #print(df['dates'].dt.day)
    print(len(df_27))
    print(len(df_28))
    plt.hist(df_27['dates'].dt.hour, bins = 9, label = r'05.10')
    plt.hist(df_28['dates'].dt.hour, bins = 13, label = r'06.10')
    plt.legend()
    plt.show()


main()