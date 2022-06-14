# %%
import numpy as np
import plotly.graph_objs as go
from ipywidgets import widgets
from plotly.subplots import make_subplots

import plotly.express as px

import scipy.io.wavfile as wf
from os import path

[rate, data] = wf.read(path.join('.', 'data', 'song_1.wav'))
Y=data[:, 0]
px.scatter(x=np.arange(len(Y)), y=Y).show()

# %%
