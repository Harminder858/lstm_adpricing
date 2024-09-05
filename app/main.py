import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from app.dashboard import (
    create_layout,
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
