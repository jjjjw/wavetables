from osc_gen import sig
from osc_gen import dsp
from lib.gen import Harmonics
from lib.filter import filter_wave

def generate_waves(wave_size, table_size):
  # Create a signal generator.
  sg = sig.SigGen(num_points=wave_size)
  harm = Harmonics(num_points=wave_size)

  waves = []

  # Basic shapes
  waves += (sg.sin(), sg.tri(), sg.saw(), sg.sqr(), sg.sharkfin(), sg.sqr_saw(), sg.exp_saw(3), sg.exp_sin(3))
  # Odd/even gradients
  waves += (dsp.mix(sg.sin(), harm.odd(), p) for p in (i / 10. for i in range(1, 9)))
  waves += (dsp.mix(sg.sin(), harm.all(), p) for p in (i / 10. for i in range(1, 9)))
  waves += (dsp.mix(sg.sin(), harm.even(), p) for p in (i / 10. for i in range(1, 9)))
  # full filtered
  waves += (filter_wave(harm.all(), p * 2, 'lowpass') for p in range(15, 47, 4))
  waves += (filter_wave(harm.all(), p * 2, 'highpass') for p in range(15, 47, 4))
  waves += (filter_wave(harm.all(), p * 2, 'bandpass') for p in range(15, 47, 4))
  waves += (filter_wave(harm.all(), p * 2, 'notch') for p in range(15, 47, 4))

  return waves