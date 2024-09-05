from dash import html, dcc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np

def create_layout(df):
    return html.Div([
        html.H1('Ad Pricing Optimization Dashboard'),
        
        dcc.DatePickerRange(
            id='date-range',
            start_date=df['date'].min(),
            end_date=df['date'].max(),
            display_format='YYYY-MM-DD'
        ),
        
        html.Div([
            html.Div([
                html.H3('Revenue Over Time'),
                dcc.Graph(id='revenue-graph')
            ], className='six columns'),
            
            html.Div([
                html.H3('Performance Metrics'),
                dcc.Graph(id='performance-metrics')
            ], className='six columns')
        ], className='row'),
        
        html.Div([
            html.Div([
                html.H3('Platform Performance'),
                dcc.Graph(id='platform-performance')
            ], className='six columns'),
            
            html.Div([
                html.H3('Ad Format Effectiveness'),
                dcc.Graph(id='format-effectiveness')
            ], className='six columns')
        ], className='row'),
        
        html.Div([
            html.H3('Bid Amount vs. ROAS'),
            dcc.Graph(id='bid-roas-scatter')
        ]),
        
        html.Div([
            html.H3('Target Audience Analysis'),
            dcc.Graph(id='audience-analysis')
        ]),
        
        html.Div([
            html.H3('Price Optimization Suggestions'),
            html.Ul(id='optimization-suggestions')
        ])
    ])

def update_revenue_graph(df, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    fig = px.line(filtered_df, x='date', y='revenue', title='Ad Revenue Over Time')
    return fig

def update_performance_metrics(df, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    metrics = [
        go.Indicator(
            mode="number+delta",
            value=filtered_df['ctr'].mean(),
            title={"text": "Avg. CTR"},
            delta={'reference': df['ctr'].mean(), 'relative': True},
            domain={'row': 0, 'column': 0}
        ),
        go.Indicator(
            mode="number+delta",
            value=filtered_df['cvr'].mean(),
            title={"text": "Avg. CVR"},
            delta={'reference': df['cvr'].mean(), 'relative': True},
            domain={'row': 0, 'column': 1}
        ),
        go.Indicator(
            mode="number+delta",
            value=filtered_df['roas'].mean(),
            title={"text": "Avg. ROAS"},
            delta={'reference': df['roas'].mean(), 'relative': True},
            domain={'row': 1, 'column': 0}
        ),
        go.Indicator(
            mode="number+delta",
            value=filtered_df['revenue'].sum(),
            title={"text": "Total Revenue"},
            delta={'reference': df['revenue'].sum(), 'relative': True},
            domain={'row': 1, 'column': 1}
        )
    ]
    layout = go.Layout(grid={'rows': 2, 'columns': 2, 'pattern': "independent"})
    return {'data': metrics, 'layout': layout}

def update_platform_performance(df, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    platform_perf = filtered_df.groupby('platform').agg({
        'revenue': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    platform_perf['ctr'] = platform_perf['clicks'] / platform_perf['impressions']
    platform_perf['cvr'] = platform_perf['conversions'] / platform_perf['clicks']
    
    fig = px.bar(platform_perf, x='platform', y=['ctr', 'cvr', 'revenue'], 
                 title='Platform Performance', barmode='group')
    return fig

def update_format_effectiveness(df, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    format_effect = filtered_df.groupby('format').agg({
        'revenue': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    format_effect['ctr'] = format_effect['clicks'] / format_effect['impressions']
    format_effect['cvr'] = format_effect['conversions'] / format_effect['clicks']
    
    fig = px.scatter(format_effect, x='ctr', y='cvr', size='revenue', color='format',
                     hover_data=['format', 'revenue', 'impressions', 'clicks', 'conversions'],
                     title='Ad Format Effectiveness')
    return fig

def update_bid_roas_scatter(df, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    fig = px.scatter(filtered_df, x='bid_amount', y='roas', color='platform', 
                     size='impressions', hover_data=['ad_id', 'format', 'target_audience'],
                     title='Bid Amount vs. ROAS')
    return fig

def update_audience_analysis(df, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    audience_perf = filtered_df.groupby('target_audience').agg({
        'revenue': 'sum',
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum'
    }).reset_index()
    
    audience_perf['ctr'] = audience_perf['clicks'] / audience_perf['impressions']
    audience_perf['cvr'] = audience_perf['conversions'] / audience_perf['clicks']
    audience_perf['roas'] = audience_perf['revenue'] / (audience_perf['impressions'] * df['bid_amount'].mean())
    
    fig = px.parallel_coordinates(audience_perf, dimensions=['target_audience', 'ctr', 'cvr', 'roas', 'revenue'],
                                  title='Target Audience Analysis')
    return fig

def generate_optimization_suggestions(df, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Identify top-performing ads
    top_ads = filtered_df.sort_values('roas', ascending=False).head(3)
    
    # Identify underperforming ads
    underperforming_ads = filtered_df[filtered_df['roas'] < 1].sort_values('roas')
    
    suggestions = [
        f"Top performing ad: {top_ads.iloc[0]['ad_id']} (ROAS: {top_ads.iloc[0]['roas']:.2f}). Consider increasing budget.",
        f"Underperforming ad: {underperforming_ads.iloc[0]['ad_id']} (ROAS: {underperforming_ads.iloc[0]['roas']:.2f}). Consider adjusting targeting or creative.",
        f"Best performing platform: {filtered_df.groupby('platform')['roas'].mean().idxmax()}. Allocate more budget to this platform.",
        f"Most effective format: {filtered_df.groupby('format')['cvr'].mean().idxmax()} for conversions. Create more ads in this format.",
        f"Optimal bid range: ${filtered_df[filtered_df['roas'] > filtered_df['roas'].median()]['bid_amount'].min():.2f} - ${filtered_df[filtered_df['roas'] > filtered_df['roas'].median()]['bid_amount'].max():.2f}. Adjust bids to fall within this range."
    ]
    
    return [html.Li(suggestion) for suggestion in suggestions]