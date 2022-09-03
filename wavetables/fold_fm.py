from osc_gen import sig
from osc_gen import dsp
import numpy as np
from lib.gen import SimpleFM
import random

def generate_waves(wave_size, table_size):
  sg = sig.SigGen(num_points=wave_size)
  fm = SimpleFM(num_points=wave_size)

  waves = []

  waves += (dsp.fold(sg.sin(), i) for i in range(1, 17, 2))
  waves += (fm.fm(depth=i) for i in range(1, 17, 2))
  waves += (dsp.fold(sg.sin(), i, bias=random.randint(0, 1)) for i in range(1, 17, 2))
  waves += (fm.fm(ratio=1, depth=i) for i in range(1, 17, 2))
  waves += (dsp.fold(fm.fm(depth=18 - 1), i) for i in range(1, 17, 2))
  waves += (dsp.fold(fm.fm(depth=i), i) for i in range(1, 17, 2))
  waves += (dsp.fold(fm.fm(depth=random.randint(0, 18)), i, bias=random.randint(0, 1)) for i in range(1, 17, 2))
  waves += (fm.fm(ratio=random.randint(0, 1), depth=i) for i in range(1, 17, 2))

  return waves