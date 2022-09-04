from osc_gen import sig
from osc_gen import dsp
from lib.gen import AdditiveGenCallback

def generate_waves(wave_size, table_size):
  waves = []

  def notch(degree=2):
    def harmonics(harmonic):
      if harmonic == 1:
        return 1
      elif harmonic < degree:
        return 0
      else:
        return 1 / harmonic
    return AdditiveGenCallback(num_points=wave_size, callback=harmonics).wave()

  def bandlimited(degree=2):
    def harmonics(harmonic):
      if harmonic == 1:
        return 1
      elif harmonic < degree:
        return 1 / harmonic
      else:
        return 0
    return AdditiveGenCallback(num_points=wave_size, callback=harmonics).wave()

  def bandpass(degree=1):
    def harmonics(harmonic):
      if harmonic == 1:
        return 1
      elif harmonic < degree or harmonic > degree + 3:
        return 0
      else:
        return 1 / harmonic
    return AdditiveGenCallback(num_points=wave_size, callback=harmonics).wave()

  def filtered_saw(degree=1):
    def harmonics(harmonic):
      if harmonic == 1:
        return 1
      else:
        return (1 / degree) / harmonic
    return AdditiveGenCallback(num_points=wave_size, callback=harmonics).wave()

  def filtered_sqr(degree=2):
    def harmonics(harmonic):
      if harmonic == 1:
        return 1
      elif harmonic % 2:
        return (1 / degree) / harmonic
      else:
        return 0
    return AdditiveGenCallback(num_points=wave_size, callback=harmonics).wave()

  def steppy(degree=2):
    def harmonics(harmonic):
      if harmonic == 1:
        return 1
      elif harmonic % degree:
        return 1 / harmonic
      else:
        return 0
    return AdditiveGenCallback(num_points=wave_size, callback=harmonics).wave()

  waves += (notch(i + 2) for i in range(1, 9))
  waves += (bandlimited(i + 2) for i in range(1, 9))
  waves += (bandpass(i) for i in range(1, 9))
  waves += (filtered_saw(i) for i in range(1, 9))
  waves += (bandlimited(i) for i in range(9, 17))
  waves += (notch(i) for i in range(9, 17))
  waves += (filtered_sqr(i) for i in range(1, 9))
  waves += (steppy(i) for i in range(1, 9))

  return waves