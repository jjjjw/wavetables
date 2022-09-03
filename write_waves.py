from osc_gen import wavetable
from osc_gen import sig
import sys
import configparser
import importlib

config = configparser.ConfigParser()
config.read('write_waves.ini')

if not config.sections():
  raise Exception('Please add a config file with output targets')

args = sys.argv
targets = config.sections()

if len(args) < 2:
  raise Exception('Please specify a script from the wavetables directory')

if len(args) < 3:
  raise Exception('Please specify a target'.format(targets))

target = args[2]
if target not in config.sections():
  raise Exception('Please specify a target in: {}'.format(targets))

target = config[target]

wave_size = target.getint('wave_size', 2048)
output_dir = target.get('output_dir', './')
table_size = target.getint('table_size', 64)
error_when_missing_waves = target.getboolean('error_when_missing_waves', False)

output_name = args[3] if len(args) == 4 else args[1]

output_loc = output_dir + '/{}.wav'.format(output_name)

script = importlib.import_module('wavetables.{}'.format(args[1]))

waves = list(script.generate_waves(wave_size, table_size))

if len(waves) != table_size and error_when_missing_waves:
  raise Exception('Please include {} waves ({} included)'.format(table_size ,len(waves)))

wt = wavetable.WaveTable(table_size, waves=waves, wave_len=wave_size)

wt.to_wav(output_loc)
