# %%
import plotly.graph_objs as go
import numpy as np
#from ipywidgets import interact, interactive
from ipywidgets import widgets
from plotly.subplots import make_subplots

import plotly.express as px

aSlider = widgets.FloatSlider(
    value=20.0,
    min=1.0,
    max=100.0,
    step=0.1,
    description='Signal:',
    continuous_update=True
)

bSlider = widgets.IntSlider(
    value=1,
    min=1,
    max=1000,
    step=1,
    description='Sampling Rate:',
    continuous_update=True
)

cSlider = widgets.IntSlider(
  value=1,
  min=0,
  max=5000,
  step=1,
  description='Sampling Offset:',
  continuous_update=True
)

fig = go.FigureWidget(make_subplots(specs=[[{"secondary_y": True}]]))
# fig.show()
fig.add_scatter()
fig.add_scatter()
xs=np.linspace(0, 1, 10000)

def response(change):
  with fig.batch_update():
    y_real = np.sin(aSlider.value*xs)
    fig.data[0].x=xs
    fig.data[0].y=y_real
    fig.data[1].x=xs[cSlider.value::bSlider.value]
    fig.data[1].y=y_real[cSlider.value::bSlider.value]

aSlider.observe(response, names="value")
bSlider.observe(response, names="value")
cSlider.observe(response, names="value")

response("")

widgets.VBox([aSlider, bSlider, cSlider, fig])

# %%
