import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from dashboard import (
    create_layout,
    update_revenue_graph,
    update_performance_metrics,
    update_platform_performance,
    update_format_effectiveness,
    update_bid_roas_scatter,
    update_audience_analysis,
    generate_optimization_suggestions
)

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the data file
data_file_path = os.path.join(current_dir, '..', 'data', 'ad_data.csv')

# Load your data here
df = pd.read_csv(data_file_path)
df['date'] = pd.to_datetime(df['date'])

app = dash.Dash(__name__)
server = app.server  # This is the line needed for Gunicorn

app.layout = create_layout(df)

# Your callback functions here
@app.callback(
    Output('revenue-graph', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_revenue_graph_callback(start_date, end_date):
    return update_revenue_graph(df, start_date, end_date)

@app.callback(
    Output('performance-metrics', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_performance_metrics_callback(start_date, end_date):
    return update_performance_metrics(df, start_date, end_date)

@app.callback(
    Output('platform-performance', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_platform_performance_callback(start_date, end_date):
    return update_platform_performance(df, start_date, end_date)

@app.callback(
    Output('format-effectiveness', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_format_effectiveness_callback(start_date, end_date):
    return update_format_effectiveness(df, start_date, end_date)

@app.callback(
    Output('bid-roas-scatter', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_bid_roas_scatter_callback(start_date, end_date):
    return update_bid_roas_scatter(df, start_date, end_date)

@app.callback(
    Output('audience-analysis', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_audience_analysis_callback(start_date, end_date):
    return update_audience_analysis(df, start_date, end_date)

@app.callback(
    Output('optimization-suggestions', 'children'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def update_optimization_suggestions_callback(start_date, end_date):
    return generate_optimization_suggestions(df, start_date, end_date)

if __name__ == '__main__':
    app.run_server(debug=True)
