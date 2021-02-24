from os import name
from numpy.core.fromnumeric import shape
import pandas as pd
import plotly.express as px

df = pd.read_csv(r'currentProcessing\currentTest02p.csv')


fig = px.line(df, x='Time', y='0', title = "currentTest")
fig.add_scatter(x=df['Time'], y=df['1']) 

fig.show()