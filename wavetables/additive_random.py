from osc_gen import sig
from osc_gen import dsp
from lib.gen import AdditiveGen
import random
import numpy as np

def generate_waves(wave_size, table_size):
  for i in range(0, table_size):
    notch = (i >= 32 and i < 40) or i >= 48
    bandpass = (i >= 40 and i < 48) or i >= 48

    gen = AdditiveGen(
      odd_perc=random.randint(1, 100) / 100, 
      even_perc=random.randint(1, 100) / 100,
      num_points=wave_size,
      odd_comb_perc=random.randint(1, 100) / 100,
      even_comb_perc=random.randint(1, 100) / 100,
      odd_comb_start=random.randint(1, int(wave_size / 2 / 4)),
      even_comb_start=random.randint(1, int(wave_size / 2 / 4)),
      odd_decay=random.randint(98, 120) / 100,
      even_decay=random.randint(98, 120) / 100,
      notch_start=random.randint(1, int(wave_size / 2 / 4)) if notch else 0,
      notch_width=random.randint(1, int(wave_size / 2 / 16)) if notch else 0,
      notch_depth=random.randint(1, 100) / 100 if notch else 0,
      bandpass_start=random.randint(1, int(wave_size / 2 / 4)) if notch else 0,
      bandpass_width=random.randint(1, int(wave_size / 2 / 16)) if notch else 0,
      bandpass_depth=random.randint(1, 100) / 10 if notch else 0
    )

    yield gen.wave()
