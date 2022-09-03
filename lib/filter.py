from scipy import signal
import numpy as np

def filter_wave(wave, cutoff, filter_type, fs=1000):
  if filter_type in ['lowpass', 'highpass']:
    sos = signal.butter(5, cutoff, filter_type, output='sos', fs=fs)
    filtered = signal.sosfilt(sos, wave)
  elif filter_type in ['bandpass', 'notch']:
    if filter_type == 'notch':
      filter_type = 'bandstop'
    sos = signal.butter(5, [cutoff, cutoff + fs / 10], filter_type, output='sos', fs=fs)
    filtered = signal.sosfilt(sos, wave)
  else:
    raise Exception('Please specify lowpass, highpass, bandpass, or notch')

  return filtered