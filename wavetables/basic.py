from osc_gen import sig
from osc_gen import dsp
from lib.gen import ShapeGen

def generate_waves(wave_size, table_size):
  # Create a signal generator.
  sg = sig.SigGen(num_points=wave_size)

  shapes = ShapeGen(num_points=wave_size)

  waves = []
  # Basic shapes:
  waves += (sg.tri(), sg.sin(), sg.saw(), sg.sqr(), shapes.zig_zag())
  # Morph between square saw:
  waves += (sg.sqr_saw(p) for p in (i / 4. for i in reversed(range(1, 4))))
  # Morph between exp sine degrees:
  waves += (sg.exp_sin(i) for i in range(1, 9))
  # Morph PWM
  waves += (sg.pls(i) for i in (i / 9. for i in range(1, 9)))
  # Morph between exp saw degrees:
  waves += (sg.exp_saw(i) for i in range(1, 9))
  # Morph between sharkfin degrees:
  waves += (sg.sharkfin(p) for p in (i / 8. for i in range(1, 9)))
  # Morph between tube saturation degrees:
  waves += (dsp.tube(sg.saw(), i) for i in range(11, 19))
  # Morph between wavefold degrees:
  waves += (dsp.fold(sg.sin(), i / 10) for i in range(11, 19))
  # Morph between polynomial shaping degrees:
  waves += (dsp.shape(sg.sin(), 1.0, power=i) for i in range(11, 19))

  return waves
