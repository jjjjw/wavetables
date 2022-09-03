from osc_gen import sig
from osc_gen import dsp
import random

def generate_waves(wave_size, table_size):
  # Create a signal generator.
  sg = sig.SigGen(num_points=wave_size)

  waves = []

  # Mix noise into various waveforms
  waves += (dsp.mix(sg.exp_sin(random.randint(1, 10)), sg.noise(character=random.randint(20, 30) / 100), amount=random.randint(20, 30) / 100) for i in range(0, 8))
  waves += (dsp.mix(sg.exp_saw(random.randint(1, 10)), sg.noise(character=random.randint(20, 30) / 100), amount=random.randint(20, 30) / 100) for i in range(0, 8))
  waves += (dsp.mix(sg.sqr_saw(random.randint(1, 10) / 10), sg.noise(character=random.randint(20, 30) / 100), amount=random.randint(20, 30) / 100) for i in range(0, 8))
  waves += (dsp.mix(sg.sin(), sg.noise(character=random.randint(20, 30) / 100), amount=random.randint(20, 30) / 100) for i in range(0, 8))
  waves += (dsp.mix(sg.tri(), sg.noise(character=random.randint(20, 30) / 100), amount=random.randint(20, 30) / 100) for i in range(0, 8))
  waves += (dsp.mix(sg.sharkfin(random.randint(1, 10) / 10), sg.noise(character=random.randint(20, 30) / 100), amount=random.randint(20, 30) / 100) for i in range(0, 8))
  waves += (dsp.mix(sg.arb(random.randint(1, 10) for i in range(0, 8)), sg.noise(character=random.randint(20, 30) / 100), amount=random.randint(20, 30) / 100) for i in range(0, 8))
  waves += (dsp.mix(sg.arb(random.randint(1, 10) for i in range(0, 16)), sg.noise(character=random.randint(20, 30) / 100), amount=random.randint(20, 30) / 100) for i in range(0, 8))

  return waves