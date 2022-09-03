# Wavetable generation scripts

Scripts for generating wavetables using the osc-gen library: https://github.com/harveyormston/osc_gen 

## Usage:

### Create a `write_waves.ini` file
First, create a `write_waves.ini` configuration file. This file will allow you to configure where the wavetables are written, the samples per wave, and the number of waves in a table. Example:

```
[ph]
wave_size=256
table_size=64
error_when_missing_waves=True
output_dir=/my/computer/PHWaves
```

### Run the write_waves script to write wavetabes
Now, you can run `write_waves.py` to generate the wavetables. The `write_waves` script can load one of the modules in the `wavetables` directory. As arguments, provide the name of the wavetable module, the target, and optionally a file name (the default is wavetable module name). Example:

`python -m write_waves odd_even ph`


### Adding a wavetable module
A file in the the `wavetables` directory needs to implement the `generate_waves` function and return a list of waves. The `generate_waves` function is passed `wave_size` and `table_size` as arguments, this way you can render waves at the best resolution and dynamically create waves to fill the table.

## Installation:
On a Mac M1 you may need this hack for locating the 'sndfile' library:
https://github.com/bastibe/python-soundfile/pull/322