# Import Libraries
from dash import Dash, html, dash_table, dcc, callback, Input, Output
import pandas as pd 
import plotly.express as px
# import dash_design_kit as ddk

# Fetch Data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the App
app = Dash()

# Build the app layout
app.layout = [
    html.Div(children="My First Dash App with Data, Graph and Controls", style={'text-align':'center'}),
    html.Hr(),
    dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id='controls-and-radio-item'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    # dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg'))
    dcc.Graph(figure={}, id='controls-and-graph'),
]

# Add controls to build interactions
@callback(
    Output(component_id='controls-and-graph', component_property='figure'), 
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
    return fig

# Run the app 
if __name__ == '__main__':
    app.run(debug=True, port=8055)