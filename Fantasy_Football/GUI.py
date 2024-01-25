import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd

# Sample data

# Replace 'your_file.csv' with the actual path to your CSV file
football_stats = '2022.csv'

# Read the CSV file and create a DataFrame
data = pd.read_csv(football_stats)

# Initialize the Dash app
app = dash.Dash(__name__)

# setting the football image online to a variable
football_image_url = 'https://live.staticflickr.com/8622/15990630063_98da2d0f1d_b.jpg'

# setting variables of the allowed columns for the different dropdown menus
allowed_columns = ['Player', 'Team']
allowed_columns2 = ['Age', 'Games Played', 'Games Started', 'Completions', 'Passing Attempts', 'Passing Yards', 'Passing TDs', 'Interceptions', 'Rushing Attempts', 'Rushing Yards', 'Rushing Yards / Attempt', 'Rushing TDs', 'Targets', 'Receptions', 'Receiving Yards', 'Yards / Reception', 'Recieving TDs', 'Fumbles', 'Fumbles Lost', 'Total TDs', '2 Point Conversions', '2 Point Conversions - Passes', 'Fantasy Points', 'VBD', 'Position Rank', 'Overall Rank', 'Total Yards', 'Completions']

# Define the layout of the app with styles
app.layout = html.Div(style={'backgroundColor': '#282c34', 'color': '#FFFFFF', 'fontFamily': 'Arial'}, children=[

    # Makes the title of the UIx
    html.H1("Football Statistics Viewer", style={'textAlign': 'center'}),

    # Sets the parameters of the imported football image from the internet
    html.Div([
        html.Img(src=football_image_url, style={'height': '300px', 'width': '500px', 'margin': 'auto', 'display': 'block'}),
    ], style={'textAlign': 'center', 'margin': 'auto'}),

    # Sets the parameters for the 3 dropdown menus
    html.Div([

        # Title of first dropdown Menu
        html.Label('Select Team or Player', style={'marginRight': '10px'}),
        # sets the Parameters of the dropdown menu using the allowed_columns variable created before
        dcc.Dropdown(
            id='x-axis',
            options=[
                {'label': col, 'value': col} for col in allowed_columns
            ],
            value='Player',
            # setting up the style
            style={'width': '200px', 'backgroundColor': '#FFFFFF', 'color': '#282c34', 'fontFamily': 'Arial','textAlign': 'center', 'margin': 'auto'},
        ),
        # Title of second dropdown Menu
        html.Label('Select Football Statistic', style={'marginRight': '10px'}),

        # sets the Parameters of the dropdown menu using the allowed_columns2 variable created before
        dcc.Dropdown(
            id='y-axis',
            options=[
                {'label': col, 'value': col} for col in allowed_columns2
            ],
            value='Age',
            style={'width': '200px', 'backgroundColor': '#FFFFFF', 'color': '#282c34', 'fontFamily': 'Arial','textAlign': 'center', 'margin': 'auto'}
        ),
        # The same format as previous dropdown menus
        html.Label('Select Graph Type', style={'marginRight': '10px'}),
        dcc.Dropdown(
            id='graph-type',
            options=[
                {'label': 'Bar Chart', 'value': 'bar'},
                {'label': 'Scatter Plot', 'value': 'scatter'}
            ],
            value='bar',
            style={'width': '200px', 'backgroundColor': '#FFFFFF', 'color': '#282c34', 'fontFamily': 'Arial','textAlign': 'center', 'margin': 'auto'}
        ),
    ], style={'textAlign': 'center', 'margin': 'auto'}),

    # Creating the title / style for the first graph and any configurations
    html.H2("Total Statistics", style={'marginTop': '30px','textAlign': 'center'}),
    dcc.Graph(
        id='selected-graph',
        config={'displayModeBar': False}  # Hide the modebar (optional)
    ),

    # Same setup as first graph section for second graph
    html.H2("Top 10", style={'marginTop': '30px','textAlign': 'center'}),
    dcc.Graph(
        id='top-10-graph',
        config={'displayModeBar': False}  # Hide the modebar (optional)
    )
])

# Define callback to update the main graph based on dropdown selections
@app.callback(
    dash.dependencies.Output('selected-graph', 'figure'),
    [dash.dependencies.Input('x-axis', 'value'),
     dash.dependencies.Input('y-axis', 'value'),
     dash.dependencies.Input('graph-type', 'value')]
)

# updates the fist graph depending on the dropdown menu and which graph is chosen
def update_graph(x_axis, y_axis, graph_type):

    # if the graph type dropdown menu is Bar then take display a bar graph using data variable
    if graph_type == 'bar':
        fig = px.bar(data, x=data[x_axis], y=data[y_axis], labels={x_axis: 'X-axis', y_axis: 'Y-axis'})
    else:
        # If the graph type is scatter then display the same data in a scatter plot
        fig = px.scatter(data, x=data[x_axis], y=data[y_axis], labels={x_axis: 'X-axis', y_axis: 'Y-axis'})


    fig.update_layout(
        # Set the background color of the graph
        plot_bgcolor='#222831',
        # Set the background color of the plot area
        paper_bgcolor='#222831',
        # Set the font color of the text
        font_color='#FFFFFF'
    )

    return fig


# Define callback to update the top 10 graph based on dropdown selections
@app.callback(
    dash.dependencies.Output('top-10-graph', 'figure'),
    [dash.dependencies.Input('x-axis', 'value'),
     dash.dependencies.Input('y-axis', 'value'),
     dash.dependencies.Input('graph-type', 'value')]
)
# updates the second graph based on the callback statments above
def update_top_10_graph(x_axis, y_axis, graph_type):

    # Select top 10 data points based on the chosen statistic
    top_10 = data.nlargest(10, columns=y_axis)

    if graph_type == 'scatter':
        fig = px.scatter(top_10, x=top_10[x_axis], y=top_10[y_axis], labels={x_axis: 'X-axis', y_axis: 'Y-axis'})
    else:
        fig = px.bar(top_10, x=top_10[x_axis], y=top_10[y_axis], labels={x_axis: 'X-axis', y_axis: 'Y-axis'})

    fig.update_layout(
        plot_bgcolor='#222831',  # Set the background color of the graph
        paper_bgcolor='#222831',  # Set the background color of the plot area
        font_color='#FFFFFF'  # Set the font color of the text
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
