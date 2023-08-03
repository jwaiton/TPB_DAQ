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


