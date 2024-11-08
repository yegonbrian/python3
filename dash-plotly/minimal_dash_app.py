from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Import the data 
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

# Initialize the app
app = Dash()

# Define the app layout: 
app.layout = [
    html.H1(children='Title of the Dash App', style={'text-align':'center'}),
    dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
]

@callback(
    Output('graph-content', 'figure'), 
    Input('dropdown-selection', 'value')
)

def update_graph(value):
    dff = df[df.country==value]
    return px.line(dff, x='year', y='pop')

if __name__ == "__main__":
    app.run(debug=True, port=8052)