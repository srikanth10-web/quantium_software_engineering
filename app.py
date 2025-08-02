import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Load and process the data
def load_data():
    df = pd.read_csv('formatted_sales_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

# Create the visualization
def create_figure(selected_region='all'):
    df = load_data()
    
    # Filter by region if not 'all'
    if selected_region != 'all':
        df = df[df['region'] == selected_region]
    
    # Group by date and calculate daily total sales
    daily_sales = df.groupby('date')['sales'].sum().reset_index()
    daily_sales = daily_sales.sort_values('date')
    
    # Add price information based on date
    def get_price(date):
        if date < pd.to_datetime('2021-01-15'):
            return 3.0
        else:
            return 5.0
    
    daily_sales['price'] = daily_sales['date'].apply(get_price)
    
    # Create the visualization
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=(f'Daily Sales Over Time - {selected_region.title()} Region', 'Price Changes'),
        vertical_spacing=0.1,
        row_heights=[0.7, 0.3]
    )
    
    # Add sales line
    fig.add_trace(
        go.Scatter(
            x=daily_sales['date'],
            y=daily_sales['sales'],
            mode='lines',
            name='Daily Sales',
            line=dict(color='#FF69B4', width=3),
            hovertemplate='<b>Date:</b> %{x}<br>' +
                         '<b>Sales:</b> $%{y:,.0f}<br>' +
                         '<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add price change line
    fig.add_trace(
        go.Scatter(
            x=daily_sales['date'],
            y=daily_sales['price'],
            mode='lines',
            name='Price',
            line=dict(color='#FF4500', width=3),
            hovertemplate='<b>Date:</b> %{x}<br>' +
                         '<b>Price:</b> $%{y}<br>' +
                         '<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Add vertical line for price change
    price_change_date = pd.to_datetime('2021-01-15')
    fig.add_vline(
        x=price_change_date,
        line_dash="dash",
        line_color="red",
        line_width=2,
        row=1, col=1
    )
    
    fig.add_vline(
        x=price_change_date,
        line_dash="dash", 
        line_color="red",
        line_width=2,
        row=2, col=1
    )
    
    # Add annotation for price change
    if len(daily_sales) > 0:
        fig.add_annotation(
            x=price_change_date,
            y=daily_sales['sales'].max() * 0.9,
            text="Price Increase:<br>$3.00 → $5.00",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="red",
            bgcolor="white",
            bordercolor="red",
            borderwidth=1,
            row=1, col=1
        )
    
    # Update layout
    fig.update_layout(
        title={
            'text': f'Pink Morsels Sales Analysis - {selected_region.title()} Region',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#2E86AB'}
        },
        xaxis_title="Date",
        yaxis_title="Daily Sales ($)",
        yaxis2_title="Price ($)",
        height=700,
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    # Update axes
    fig.update_xaxes(title_text="Date", row=2, col=1, gridcolor='lightgray')
    fig.update_yaxes(title_text="Daily Sales ($)", row=1, col=1, gridcolor='lightgray')
    fig.update_yaxes(title_text="Price ($)", row=2, col=1, gridcolor='lightgray')
    
    return fig

# App layout with enhanced styling
app.layout = html.Div([
    # Header with gradient background
    html.Div([
        html.H1("🍬 Soul Foods - Pink Morsels Sales Analysis", 
                className='main-header'),
        html.P("Interactive Regional Sales Dashboard", 
               className='subtitle')
    ], className='header-container'),
    
    # Main content container
    html.Div([
        # Left sidebar for controls
        html.Div([
            html.Div([
                html.H3("🎯 Region Filter", className='control-title'),
                html.P("Select a region to filter the data:", className='control-description'),
                dcc.RadioItems(
                    id='region-filter',
                    options=[
                        {'label': '🌍 All Regions', 'value': 'all'},
                        {'label': '🧭 North Region', 'value': 'north'},
                        {'label': '🌅 East Region', 'value': 'east'},
                        {'label': '🌞 South Region', 'value': 'south'},
                        {'label': '🌄 West Region', 'value': 'west'}
                    ],
                    value='all',
                    className='radio-items'
                )
            ], className='control-panel'),
            
            html.Div([
                html.H3("📊 Key Insights", className='insights-title'),
                html.Div(id='insights-content', className='insights-content')
            ], className='insights-panel')
        ], className='sidebar'),
        
        # Main chart area
        html.Div([
            html.Div([
                html.H3("📈 Sales Performance Analysis", className='chart-title'),
                dcc.Graph(
                    id='sales-chart',
                    className='main-chart'
                )
            ], className='chart-container'),
            
            html.Div([
                html.H4("💡 Analysis Summary", className='summary-title'),
                html.Div(id='summary-content', className='summary-content')
            ], className='summary-container')
        ], className='main-content')
    ], className='content-wrapper')
], className='app-container')

# Callback to update the chart based on region selection
@app.callback(
    [Output('sales-chart', 'figure'),
     Output('insights-content', 'children'),
     Output('summary-content', 'children')],
    [Input('region-filter', 'value')]
)
def update_chart(selected_region):
    df = load_data()
    
    # Filter by region if not 'all'
    if selected_region != 'all':
        df_filtered = df[df['region'] == selected_region]
    else:
        df_filtered = df
    
    # Calculate insights
    price_change_date = pd.to_datetime('2021-01-15')
    before_data = df_filtered[df_filtered['date'] < price_change_date]
    after_data = df_filtered[df_filtered['date'] >= price_change_date]
    
    before_avg = before_data['sales'].mean() if len(before_data) > 0 else 0
    after_avg = after_data['sales'].mean() if len(after_data) > 0 else 0
    
    sales_change = ((after_avg - before_avg) / before_avg * 100) if before_avg > 0 else 0
    
    # Create insights
    insights = [
        html.Div([
            html.Span("💰 Price Increase: ", className='insight-label'),
            html.Span("$3.00 → $5.00 (+66.7%)", className='insight-value')
        ], className='insight-item'),
        html.Div([
            html.Span("📈 Sales Before: ", className='insight-label'),
            html.Span(f"${before_avg:,.0f}", className='insight-value')
        ], className='insight-item'),
        html.Div([
            html.Span("📊 Sales After: ", className='insight-label'),
            html.Span(f"${after_avg:,.0f}", className='insight-value')
        ], className='insight-item'),
        html.Div([
            html.Span("🎯 Sales Change: ", className='insight-label'),
            html.Span(f"{sales_change:+.1f}%", 
                     className='insight-value positive' if sales_change >= 0 else 'insight-value negative')
        ], className='insight-item')
    ]
    
    # Create summary
    summary_text = f"""
    The {selected_region.title()} region shows {'an increase' if sales_change >= 0 else 'a decrease'} in daily sales 
    after the price increase on January 15, 2021. {'This suggests the price increase was successful' if sales_change >= 0 else 'This indicates the price increase may have negatively impacted demand'} 
    in this region. The data demonstrates how regional market dynamics can vary significantly 
    in response to pricing changes.
    """
    
    summary = html.P(summary_text, className='summary-text')
    
    return create_figure(selected_region), insights, summary

# CSS styles
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        <title>Soul Foods - Pink Morsels Analysis</title>
        <style>
            /* Global styles */
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            
            /* App container */
            .app-container {
                min-height: 100vh;
                padding: 20px;
            }
            
            /* Header styles */
            .header-container {
                text-align: center;
                background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
                color: white;
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            
            .main-header {
                font-size: 2.5em;
                font-weight: bold;
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            
            .subtitle {
                font-size: 1.2em;
                opacity: 0.9;
                font-style: italic;
            }
            
            /* Content wrapper */
            .content-wrapper {
                display: flex;
                gap: 30px;
                max-width: 1400px;
                margin: 0 auto;
            }
            
            /* Sidebar */
            .sidebar {
                width: 300px;
                flex-shrink: 0;
            }
            
            .control-panel, .insights-panel {
                background: white;
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 20px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .control-title, .insights-title {
                color: #2E86AB;
                margin-bottom: 15px;
                font-size: 1.3em;
                border-bottom: 2px solid #FF69B4;
                padding-bottom: 10px;
            }
            
            .control-description {
                color: #666;
                margin-bottom: 20px;
                font-size: 0.9em;
            }
            
            /* Radio items */
            .radio-items {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            
            .radio-items label {
                display: flex;
                align-items: center;
                padding: 12px 15px;
                background: #f8f9fa;
                border-radius: 10px;
                cursor: pointer;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }
            
            .radio-items label:hover {
                background: #e9ecef;
                border-color: #FF69B4;
                transform: translateX(5px);
            }
            
            .radio-items input[type="radio"] {
                margin-right: 10px;
                accent-color: #FF69B4;
            }
            
            /* Insights */
            .insights-content {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            
            .insight-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #FF69B4;
            }
            
            .insight-label {
                font-weight: bold;
                color: #2E86AB;
            }
            
            .insight-value {
                font-weight: bold;
                color: #333;
            }
            
            .insight-value.positive {
                color: #28a745;
            }
            
            .insight-value.negative {
                color: #dc3545;
            }
            
            /* Main content */
            .main-content {
                flex: 1;
            }
            
            .chart-container {
                background: white;
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 20px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .chart-title {
                color: #2E86AB;
                margin-bottom: 20px;
                font-size: 1.5em;
                text-align: center;
            }
            
            .main-chart {
                border-radius: 10px;
                overflow: hidden;
            }
            
            /* Summary */
            .summary-container {
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            
            .summary-title {
                color: #2E86AB;
                margin-bottom: 15px;
                font-size: 1.3em;
                border-bottom: 2px solid #FF69B4;
                padding-bottom: 10px;
            }
            
            .summary-text {
                color: #555;
                line-height: 1.6;
                font-size: 1em;
            }
            
            /* Responsive design */
            @media (max-width: 1200px) {
                .content-wrapper {
                    flex-direction: column;
                }
                
                .sidebar {
                    width: 100%;
                }
            }
            
            @media (max-width: 768px) {
                .main-header {
                    font-size: 2em;
                }
                
                .app-container {
                    padding: 10px;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050) 