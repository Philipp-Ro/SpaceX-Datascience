# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                            {'label': 'All Sites', 'value': 'ALL'},
                                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                        ],
                                                value='ALL',
                                                placeholder="select launch site",
                                                searchable=True
                                ),
    
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(    id='payload-slider',
                                                    min=0, max=10000, step=1000,
                                                    marks={0: '0',
                                                        100: '100'},
                                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    #filtered_df = spacex_df
    if entered_site == 'ALL':
        all_sites =spacex_df.groupby("Launch Site").sum()
        fig = px.pie(all_sites , values='class', 
        names=pd.unique(spacex_df['Launch Site']), 
        title='Successfull launches per Launch Site')
        return fig
    else:
        filtered_df = spacex_df.where(spacex_df["Launch Site"] == entered_site)
        dict_site = filtered_df["class"].value_counts()
        fig = px.pie(dict_site, values='count', 
        names=['0','1'], 
        title='All Lauches of '+entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site,payload_vals):
    min_load= payload_vals[0]
    max_load= payload_vals[1]
    if entered_site == 'ALL':
        spaceX_payload = spacex_df.where(spacex_df["Payload Mass (kg)"].between(min_load,max_load))
        fig = px.scatter(spaceX_payload , x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig
    else:
        filtered_df = spacex_df.where(spacex_df["Launch Site"] == entered_site)
        spaceX_payload = filtered_df .where(filtered_df ["Payload Mass (kg)"].between(min_load,max_load))
        fig = px.scatter(spaceX_payload , x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig
# Run the app
if __name__ == '__main__':
    app.run_server()
