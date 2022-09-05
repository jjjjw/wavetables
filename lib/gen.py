from osc_gen import sig
from osc_gen import dsp
import numpy as np

class AdditiveGen(object):
  """Parameterized additive generator"""
  def __init__(self, 
    # Amp of fundamental
    fundament_perc=1, 
    # Tilt of all harmonics. 1 is saw like. <1 harmonics roll off faster, >1 slower (linear)
    tilt=1, 
    # Amp of odd harmonics
    odd_perc=1, 
    # Amp of even harmonics
    even_perc=1,
    # Number of samples
    num_points=2048,
    # Amp inversion of every other odd harmonic
    odd_comb_perc=0,
    # Amp inversion of every other even harmonic
    even_comb_perc=0,
    # When to start filtering every other odd harmonic
    odd_comb_start=0,
    # When to start filtering every other even harmonic
    even_comb_start=0,
    # Decay of odd harmonics. 1 is saw like. >1 harmonics roll off faster, <1 slower (exponential)
    odd_decay=1,
    # Decay of even harmonics. 1 is saw like. >1 harmonics roll off faster, <1 slower (exponential)
    even_decay=1,
    # Notch, dampen all harmonics in the range by the depth amount
    notch_start=0,
    notch_width=0,
    notch_depth=1,
    # Bandpass, dampen all harmonics in the range by the depth amount
    bandpass_start=0,
    bandpass_width=0,
    bandpass_depth=1):

    self.samples = num_points
    self.partials = int(self.samples / 2)

    self.sg = sig.SigGen(num_points=self.samples)
    self.cached_wave = None

    self.fundament_perc =  fundament_perc
    self.tilt = tilt

    self.odd_perc = odd_perc
    self.even_perc = even_perc

    self.odd_comb_start = odd_comb_start
    self.even_comb_start = even_comb_start

    self.odd_comb_perc = odd_comb_perc
    self.even_comb_perc = even_comb_perc

    self.odd_decay = odd_decay
    self.even_decay = even_decay

    self.notch_start = notch_start
    self.notch_width = notch_width
    self.notch_depth = notch_depth

    self.bandpass_start = bandpass_start
    self.bandpass_width = bandpass_width
    self.bandpass_depth = bandpass_depth

    # Blunt way to keep track of every other even/odd
    self.odd_comb = None
    self.even_comb = None

  def handle_harmonic(self, harmonic, decay, perc, comb, comb_perc):
    """Get the amplitude of the harmonic partial"""
    amp = (self.tilt / (harmonic ** decay)) * perc

    if comb and comb_perc:
      amp = amp * -1 * comb_perc

    if self.notch_start and self.notch_width and self.notch_depth:
      # Filter all harmonics in the notch by the depth amount
      if harmonic >= self.notch_start and harmonic < self.notch_start + self.notch_width:
        amp = amp - (amp * self.notch_depth)

    if self.bandpass_start and self.bandpass_width and self.bandpass_depth:
      # Filter all harmonics not in the bandpass by the depth amount
      if harmonic <= self.bandpass_start or harmonic > self.bandpass_start + self.bandpass_width:
        amp = amp - (amp * self.bandpass_depth)

    return amp

  def handle_odd(self, harmonic):
    amp = self.handle_harmonic(harmonic, self.odd_decay, self.odd_perc, self.odd_comb, self.odd_comb_perc)
    if self.odd_comb is not None:
      self.odd_comb = not self.odd_comb
    return amp

  def handle_even(self, harmonic):
    amp = self.handle_harmonic(harmonic, self.even_decay, self.even_perc, self.even_comb, self.even_comb_perc)
    if self.even_comb is not None:
      self.even_comb = not self.even_comb
    return amp

  def wave(self):
    if self.cached_wave is not None:
      return self.cached_wave

    # Initialize
    outp = np.zeros(self.samples)

    self.odd_comb = None
    self.even_comb = None

    # Get amp for partials
    for partial in range(0, self.partials):
      harmonic = partial + 1 # harmonics are not 0 indexed

      # Set up the "comb" filter
      if self.odd_comb is None and harmonic >= self.odd_comb_start:
        self.odd_comb = True
      if self.even_comb is None and harmonic >= self.even_comb_start:
        self.even_comb = True

      if harmonic == 1:
        # Fundamental
        amp = 1 * self.fundament_perc

      elif harmonic % 2:
        amp = self.handle_odd(harmonic)

      elif not harmonic % 2:
        amp = self.handle_even(harmonic)

      # Add amp to output
      self.sg.harmonic = partial
      self.sg.amp = amp
      outp += self.sg.sin()

    self.cached_wave = dsp.normalize(outp)      
    return self.cached_wave

class AdditiveGenCallback(AdditiveGen):
  """Create partials from a callback function"""
  def __init__(self, callback=None, **kwargs):
    AdditiveGen.__init__(self, **kwargs)
    self.callback = callback

  def handle_harmonic(self, *args):
    return self.callback(self, *args)

class Harmonics(sig.SigGen):
  """Simple odd/even/all harmonics"""
  def __init__(self, **kwargs):
    sig.SigGen.__init__(self, **kwargs)
    self.odd_wave = None

  def odd(self):
    if self.odd_wave is not None:
      return self.odd_wave
    else:
      self.odd_wave = AdditiveGen(num_points=self.num_points, even_perc=0, fundament_perc=0).wave()
      return self.odd_wave

  def even(self):
    return sig.SigGen(num_points=self.num_points, harmonic=1).saw()

  def all(self):
    return self.saw()

class SimpleFM(sig.SigGen):
  """Simple 2 op FM with sines"""

  def fm(self, ratio=0, depth=10):
    carrier = sig.SigGen(num_points=self.num_points)
    modulator = sig.SigGen(num_points=self.num_points, harmonic=ratio)

    return np.cos(carrier.sin() + (depth * modulator.sin()))

def biased_invert(inp, symmetry=0):
  """Invert half of a wave"""
  samples = np.sort(np.extract((inp < symmetry) & (inp >= symmetry - 1), inp))
  bias = samples[-1] - samples[0]
  return np.where((inp < symmetry) & (inp >= symmetry - 1), -1 * inp - bias, inp)

def biased_flip(inp, symmetry=0):
  """Flip half of a wave"""
  samples = np.where((inp < symmetry) & (inp >= symmetry - 1))[0]
  flipped = np.flip(samples)
  output = np.copy(inp)
  for ii, yy in enumerate(samples):
    output[yy] = inp[flipped[ii]]
  return output

class ShapeGen(sig.SigGen):
  """Extended SigGen for custom shapes"""
  def zig_zag(self):
    return biased_invert(self.saw())

