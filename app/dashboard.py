import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import html, dcc

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
            html.H3('Target Audience Analysis'),
            dcc.Graph(id='audience-analysis')
        ]),
        
        html.Div([
            html.H3('Price Optimization Suggestions'),
            html.Ul(id='optimization-suggestions')
        ])
    ])

def update_audience_analysis(df, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    audience_perf = filtered_df.groupby('target_audience').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'spend': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    audience_perf['ctr'] = audience_perf['clicks'] / audience_perf['impressions']
    audience_perf['cvr'] = audience_perf['conversions'] / audience_perf['clicks']
    audience_perf['roas'] = audience_perf['revenue'] / audience_perf['spend']
    
    fig = px.parallel_coordinates(audience_perf, 
                                  dimensions=['target_audience', 'ctr', 'cvr', 'roas', 'revenue'],
                                  labels={
                                      'target_audience': 'Target Audience',
                                      'ctr': 'CTR',
                                      'cvr': 'CVR',
                                      'roas': 'ROAS',
                                      'revenue': 'Revenue'
                                  },
                                  title='Target Audience Performance',
                                  color='roas',
                                  color_continuous_scale=px.colors.sequential.Viridis)
    
    fig.update_traces(
        dimensiondefaults=dict(
            tickformat='.2%',
            ticksuffix='',
            range_color=[audience_perf['roas'].min(), audience_perf['roas'].max()]
        )
    )
    
    fig.update_layout(
        coloraxis_colorbar=dict(
            title='ROAS',
            tickformat='.2f'
        )
    )
    
    # Format the revenue axis
    fig.update_layout(
        {f'parcats{i}': dict(tickformat='$.2f', ticksuffix='M') 
         for i in range(len(fig.data)) if fig.data[i].dimensions[4].label == 'Revenue'}
    )
    
    return fig

def generate_optimization_suggestions(df, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # Identify top-performing ads
    top_ads = filtered_df.sort_values('roas', ascending=False).head(3)
    
    # Identify underperforming ads
    underperforming_ads = filtered_df[filtered_df['roas'] < 1].sort_values('roas')
    
    # Identify best performing platform and format
    best_platform = filtered_df.groupby('platform')['roas'].mean().idxmax()
    best_format = filtered_df.groupby('format')['cvr'].mean().idxmax()
    
    # Calculate optimal bid range
    optimal_bids = filtered_df[filtered_df['roas'] > filtered_df['roas'].median()]['bid_amount']
    optimal_bid_range = (optimal_bids.min(), optimal_bids.max())
    
    suggestions = [
        f"Top performing ad: {top_ads.iloc[0]['ad_id']} (ROAS: {top_ads.iloc[0]['roas']:.2f}). Consider increasing budget.",
        f"Underperforming ad: {underperforming_ads.iloc[0]['ad_id']} (ROAS: {underperforming_ads.iloc[0]['roas']:.2f}). Consider adjusting targeting or creative.",
        f"Best performing platform: {best_platform}. Allocate more budget to this platform.",
        f"Most effective format: {best_format} for conversions. Create more ads in this format.",
        f"Optimal bid range: ${optimal_bid_range[0]:.2f} - ${optimal_bid_range[1]:.2f}. Adjust bids to fall within this range."
    ]
    
    return [html.Li(suggestion) for suggestion in suggestions]
