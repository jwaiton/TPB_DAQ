# TPB_DAQ
Currently a repository dedicated to working around lecroys stupid TRC files and using python for basic baseline subtraction. 


### parse_data.py

Takes folder of TRC files and creates integrated charge histogram, outputs to output/run_NN folder integrated data and basic plot.

### parse_data_waveforms.py

Takes folder of TRC files and creates dumb waveform data, outputs to output_waveforms/run_NN folder waveform plotting data. Use in conjunction with plot_data.py.

### plot_data.py

More precise plotting control for .npy files

### find_peaks.py

Peak finding algorithm, will be looked at more significantly soon. Uses .npy files created by *parse_data.py*

### analyse_trc.py

Simple script that outputs plot and ADC score for any TRC file passed to it.
Assuming file structure matches expected 'C1--PMT-test_calibration_long--' format.

### plot_data_points.py

Automated plotting script, will continuously plot.

### process_waveforms.py

Basic script to bin waveforms, and subtract one waveform from another for plotting. Used for background subtraction plots.

### marc_binning.py

Binning method stripped form Marc Seeman's Masters project found [here](https://github.com/MarcSeemann/Mphys-Project)

#### Reformatting

As part of a process to make the repo less script-heavy. Planning to take most major functions and put them in a well documented 'PMT_func.py' file. These two files are the beginning of this process.

### data_binning.py

Simple binning script that may or may not work

### subtract_waveforms.py

Simple subtraction application.
