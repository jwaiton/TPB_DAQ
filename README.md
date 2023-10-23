# TPB_DAQ
Currently a repository dedicated to working around lecroys TRC files and using python for basic baseline subtraction. 
The current format consists of folders that contain example files, output files, obsolete and relevant scripts, and miscellaneous documentation.

---

## Folders

### TPC_lab_testing
TRC files containing PMT waveforms from a lecroy waverunner 8000 series oscilloscope. Used for testing certain scripts dependent on said TRCs.

### core
Folder containing the basic functions used to run most relevant scripts in this repository. (Hopefully) well documented for adaptability.

### docs
Documentation for the core functions (WIP)

### obs
Obsolete functions still kept for being useful in the future

### output
Output from processing PMT waveforms, consisting of charge integrals

### output waveforms
Output from processing PMT waveforms, consisting of averaged waveforms

### testing_output
Bin for useless outputs from scripts

---

## Scripts

### analyse_trc.py

Simple script that outputs plot and ADC score for any TRC file passed to it.
Assuming file structure matches expected 'C1--PMT-test_calibration_long--' format.

### apply_fits.py

Script that applies 2 gaussian fits to charge histogram .npy data. Can be adapted for N gaussian fits.

### data_binning.py

Binning script that has untested functionality.

### parse_data.py/parse_dat.py

Takes folder of TRC files and creates integrated charge histogram, outputs to output/run_NN folder integrated data and basic plot.
*Two versions currently exist. _data is original working version, _dat is version using core/processing functions and may be buggy*

### parse_data_waveforms.py

Takes folder of TRC files and creates dumb waveform data, outputs to output_waveforms/run_NN folder waveform plotting data. Use in conjunction with plot_data.py.

### plot_events.py

Plots TRC files iteratively from PATH

### process_waveforms.py

Subtract one waveform from another and then view these subtracted waveforms and save them. Simple script, should be absorbed into something else

## Plotting

Couple of bespoke scripts for plotting specific data.

### plot_data.py

More precise plotting control for .npy files

### plot_data_chargeInt.py

Simple histogram plot for charge integral .npy data

### plot_data_waveforms.py

Waveform plotter with pedestal subtraction via median.

### plot_data_points.py

Plots output .trc files from oscilloscope.


## Reformatting

As part of a process to make the repo less script-heavy. Planning to take most major functions and put them in a well documented 'PMT_func.py' file. These two files are the beginning of this process.

### marc_binning.py

Binning method stripped form Marc Seeman's Masters project found [here](https://github.com/MarcSeemann/Mphys-Project)




### subtract_waveforms.py

Simple subtraction application.
