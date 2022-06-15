# %%
import plotly.graph_objs as go
import numpy as np
#from ipywidgets import interact, interactive
from ipywidgets import widgets
from plotly.subplots import make_subplots

import plotly.express as px

COUNT_SAMPLES=10_000
signal_hz_ctrl = widgets.FloatSlider(
    value=20.0,
    min=1.0,
    max=100.0,
    step=0.1,
    description='Signal:',
    continuous_update=True
)

pilot_hz_ctrl = widgets.IntSlider(
    value=20,
    min=1,
    max=100,
    step=1,
    description='Pilot Freq:',
    continuous_update=True
)

signal_fig = go.FigureWidget(
  make_subplots(specs=[[{"secondary_y": True}]])
)
signal_fig.add_scatter()
signal_fig.add_scatter()
sin_txf_fig = go.FigureWidget(layout_yaxis_range=[-0.5,0.5])
scatter = sin_txf_fig.add_scatter(x=[-1,1], y=[-1,1])
scatter = sin_txf_fig.add_scatter()

signal_samples=np.linspace(0, 4, COUNT_SAMPLES)
fq_samples=np.linspace(1, 100, 100)

def compute_sine_transform(signal, pilot_fq):
  return signal * np.sin(pilot_fq*signal_samples) / COUNT_SAMPLES

def response(change):
  with signal_fig.batch_update(), sin_txf_fig.batch_update():
    signal = np.sin(signal_hz_ctrl.value*signal_samples)
    pilot = np.sin(pilot_hz_ctrl.value*signal_samples)
    sin_txf_samples = [sum(compute_sine_transform(signal, x)) for x in fq_samples]
    signal_fig.data[0].x=signal_samples
    signal_fig.data[0].y=signal
    signal_fig.data[1].x=signal_samples
    signal_fig.data[1].y=pilot
    sin_txf_fig.data[0].x=fq_samples
    sin_txf_fig.data[0].y=sin_txf_samples
    sin_txf_fig.data[1].x=[pilot_hz_ctrl.value]
    sin_txf_fig.data[1].y=[sin_txf_samples[pilot_hz_ctrl.value-1]]


signal_hz_ctrl.observe(response, names="value")
pilot_hz_ctrl.observe(response, names="value")

response("")

widgets.VBox([signal_hz_ctrl, pilot_hz_ctrl, signal_fig, sin_txf_fig])

# %%
