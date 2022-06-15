# %%
import numpy as np
import pandas as pd

import plotly.express as px

import scipy.io.wavfile as wf
import scipy.signal as sg
from os import path

[RATE, data] = wf.read(path.join('.', 'data', 'song_1.wav'))
Y=data[:, 0]
# px.scatter(x=np.arange(len(Y)), y=Y).show()

def sec2samp(second):
  return int(44_100*second)

def samp2sec(samp):
  return samp/44_100

fq = 5000 # hz
stf_samp = sec2samp(4)
window_len = 89 # about 20ms

comp = 0

# a 44.1kHz sine wave, y=sin(2pi * 44_100 * x)
# to sample it at the nyquist frequency, half of it, you need to go at y=sin(pi * 44_100 * x), if x is an integer number
# we can now think in terms of ratios to 44_100. for example, 5000 is 5000/44_100th the rate that 44_100 is = roughly 11%. So we can just divide our rate by fq

def window_fn(i):
  return 1

# up to a little beneath the nyquist fq
fq_bank = [22*i*10 for i in range(1,101)]

snapshots = []
timestamp = []
frequencies = []
print('computing...')
for _ in range(1, 1000):
  stf_samp += 150
  for fq in fq_bank:
    for i in range(stf_samp, stf_samp+window_len):
      comp += Y[i]*np.sin(np.pi*RATE/fq*i) #*window_fn(i)

    comp /= 89
    snapshots.append(comp)
    frequencies.append(fq)
  timestamp.extend(np.zeros(100) + stf_samp)
print('rendering...')
frame=pd.DataFrame({
  'timestamp': samp2sec(np.array(timestamp)),
  'frequencies': frequencies,
  'presence': 20*np.log10(np.abs(snapshots))
})

px.scatter(frame, x='timestamp', y='frequencies', color='presence').show()

# %%
