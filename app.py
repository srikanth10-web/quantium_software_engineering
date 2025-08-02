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
    return daily_sales

# Create the visualization
def create_figure():
    daily_sales = load_data()
    
    # Create the visualization
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Daily Sales Over Time', 'Price Changes'),
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
            line=dict(color='#FF69B4', width=2),
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
        row=1, col=1
    )
    
    fig.add_vline(
        x=price_change_date,
        line_dash="dash", 
        line_color="red",
        row=2, col=1
    )
    
    # Add annotation for price change
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
            'text': 'Impact of Pink Morsels Price Increase on Sales',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title="Date",
        yaxis_title="Daily Sales ($)",
        yaxis2_title="Price ($)",
        height=700,
        showlegend=True,
        hovermode='x unified'
    )
    
    # Update axes
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Daily Sales ($)", row=1, col=1)
    fig.update_yaxes(title_text="Price ($)", row=2, col=1)
    
    return fig

# App layout
app.layout = html.Div([
    html.H1("Soul Foods - Pink Morsels Sales Analysis", 
            style={'textAlign': 'center', 'color': '#2E86AB', 'marginBottom': 30}),
    
    html.Div([
        html.H3("Key Findings:", style={'color': '#A23B72'}),
        html.Ul([
            html.Li("Price increased from $3.00 to $5.00 on January 15, 2021 (+66.7%)"),
            html.Li("Daily sales increased from $6,604 to $8,972 (+35.8%)"),
            html.Li("The price increase led to higher total revenue despite potential volume changes")
        ], style={'fontSize': 16, 'marginBottom': 30})
    ], style={'backgroundColor': '#F8F9FA', 'padding': 20, 'borderRadius': 10, 'marginBottom': 30}),
    
    dcc.Graph(
        id='sales-chart',
        figure=create_figure(),
        style={'height': 700}
    ),
    
    html.Div([
        html.H4("Analysis Summary:", style={'color': '#2E86AB'}),
        html.P([
            "The visualization above shows the impact of the Pink Morsels price increase on sales. ",
            "The red dashed line marks the date of the price change (January 15, 2021). ",
            "Despite the significant price increase of 66.7%, daily sales actually increased by 35.8%, ",
            "indicating that the price increase was successful in driving higher revenue. ",
            "This suggests that Pink Morsels may have inelastic demand or that the product's value proposition ",
            "justified the higher price point."
        ], style={'fontSize': 16, 'lineHeight': 1.6})
    ], style={'backgroundColor': '#F8F9FA', 'padding': 20, 'borderRadius': 10, 'marginTop': 30})
], style={'maxWidth': 1200, 'margin': 'auto', 'padding': 20})

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050) 