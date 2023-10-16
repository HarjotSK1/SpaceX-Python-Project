# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# TASK 1: Dropdown
launch_sites = spacex_df['Launch Site'].unique().tolist()
launch_site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites]

site_dropdown = dcc.Dropdown(id='site-dropdown',
                             options=launch_site_options,
                             value='ALL',
                             placeholder="Select a Launch Site here",
                             searchable=True)

# TASK 3: Range Slider
payload_slider = dcc.RangeSlider(id='payload-slider',
                                 min=0,
                                 max=10000,
                                 step=1000,
                                 marks={i: f'{i}' for i in range(0, 10001, 1000)},
                                 value=[min_payload, max_payload])

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                site_dropdown,
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                payload_slider,
                                html.Br(),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2: Callback for Pie Chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Success Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        counts = filtered_df['class'].value_counts().reset_index()
        counts.columns = ['class', 'count']
        fig = px.pie(counts, values='count', names='class', title=f"Launch Outcomes for {entered_site}")
    return fig

# TASK 4: Callback for Scatter Chart
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def plot_scatter(entered_site, payload_range):
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', 
                     title=f"Payload vs. Outcome for {entered_site}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
