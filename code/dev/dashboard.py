# Import packages
from dash import Dash, html, dash_table, dcc, Input, Output, callback
import plotly.graph_objects as go
import pandas as pd
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Incorporate data
df = pd.read_csv('../data/food_trucks.csv')
df2 = pd.read_csv('../data/directions_driving.csv')
# create fig
import json
with open('tokens.json') as f:
    data = json.load(f)
    GOOGLE_API_KEY = data['GOOGLE_API_KEY']
    MAP_TOKEN = data['MAP_TOKEN']
# mapbox_access_token = open(".mapbox_token").read()
latitudePts = df['lat'].tolist()
longitudePts = df['lng'].tolist()
names = df['name'].tolist()
df['rating']
techpoint = {
    "name": "techpoint",
    "location": {
        'lat': 39.78728396765869,
        'lng': -86.18316063589883}
}
fig = go.Figure(go.Scattermapbox(
    lat=latitudePts + [techpoint['location']['lat']],
    lon=longitudePts + [techpoint['location']['lng']],
    mode='markers',
    marker=go.scattermapbox.Marker(
        size=9
    ),
    text=names + [techpoint['name']],
))

fig.update_layout(
    autosize=False,
    width=1600,
    height=800,
    hovermode='closest',
    mapbox=dict(
        accesstoken=MAP_TOKEN,
        bearing=0,
        center=dict(
            lat=techpoint['location']['lat'],
            lon=techpoint['location']['lng']
        ),
        pitch=0,
        zoom=10
    ),
)

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1(children='Data Dashboard'),
    html.Div(children='Create your trip automatically'),
    html.H3(children='Rateing Selecter'),
    dcc.RangeSlider(0, 5, 1, value=[0, 5], id='slider'),
    dcc.Graph(id = 'map', figure=fig),
    html.H3(children='Details of each trucks'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=100),
    html.H3(children='Distances between each trucks'),
    dash_table.DataTable(data=df2.to_dict('records'), page_size=100),
])

@callback(
    [Output('map', 'figure')],
    [Input('slider', 'value')]
)
def update_plot(slider_range):
    # change the size column name to whatever it is for you
    col = 'rating'

    data_filtered = df.where((df[col] >= slider_range[0]) & (df[col] <= slider_range[1]))
    latitudePts = data_filtered['lat'].tolist()
    longitudePts = data_filtered['lng'].tolist()
    names = data_filtered['name'].tolist()
    # customize the figure
    fig = go.Figure(go.Scattermapbox(
        lat=latitudePts + [techpoint['location']['lat']],
        lon=longitudePts + [techpoint['location']['lng']],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=names + [techpoint['name']],
    ))

    fig.update_layout(
        autosize=False,
        width=1600,
        height=800,
        hovermode='closest',
        mapbox=dict(
            accesstoken=MAP_TOKEN,
            bearing=0,
            center=dict(
                lat=techpoint['location']['lat'],
                lon=techpoint['location']['lng']
            ),
            pitch=0,
            zoom=10
        ),
    )

    return [fig]
# Run the app
if __name__ == '__main__':
    app.run(debug=True)
