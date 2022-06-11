# %%
import plotly.graph_objs as go
import numpy as np
#from ipywidgets import interact, interactive
from ipywidgets import widgets
from plotly.subplots import make_subplots

import plotly.express as px

signal_hz_ctrl = widgets.FloatSlider(
    value=20.0,
    min=1.0,
    max=100.0,
    step=0.1,
    description='Signal:',
    continuous_update=True
)

pilot_hz_ctrl = widgets.FloatSlider(
    value=20.0,
    min=1.0,
    max=100.0,
    step=0.1,
    description='Pilot Freq:',
    continuous_update=True
)

signal_fig = go.FigureWidget(
  make_subplots(specs=[[{"secondary_y": True}]])
)
signal_fig.add_scatter()
signal_fig.add_scatter()
sin_txf_fig = go.FigureWidget(layout_yaxis_range=[-10000,10000])
scatter = sin_txf_fig.add_scatter(x=[-1,1], y=[-5000,5000])

COUNT_SAMPLES=10_000
signal_samples=np.linspace(0, 1, COUNT_SAMPLES)

def compute_sine_transform(signal, pilot_fq):
  return signal * np.sin(pilot_fq*signal_samples)

def response(change):
  with signal_fig.batch_update(), sin_txf_fig.batch_update():
    signal = np.sin(signal_hz_ctrl.value*signal_samples)
    pilot= np.sin(pilot_hz_ctrl.value*signal_samples)
    signal_fig.data[0].x=signal_samples
    signal_fig.data[0].y=signal
    signal_fig.data[1].x=signal_samples
    signal_fig.data[1].y=pilot
    sin_txf_fig.data[0].x=np.linspace(-15, 15, 30)
    sin_txf_fig.data[0].y=[sum(compute_sine_transform(signal, x + pilot_hz_ctrl.value)) for x in np.linspace(-15, 15, 30)]

signal_hz_ctrl.observe(response, names="value")
pilot_hz_ctrl.observe(response, names="value")

response("")

widgets.VBox([signal_hz_ctrl, pilot_hz_ctrl, signal_fig, sin_txf_fig])

# %%
