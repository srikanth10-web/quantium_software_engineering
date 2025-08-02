import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

def create_sales_visualization():
    """
    Create a line chart visualization showing the impact of Pink Morsels price increase on sales.
    """
    
    # Read the formatted sales data
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
    
    # Save the plot
    fig.write_html('pink_morsels_sales_analysis.html')
    fig.write_image('pink_morsels_sales_analysis.png', width=1200, height=700)
    
    print("✅ Visualization created successfully!")
    print("📊 Files saved:")
    print("   - pink_morsels_sales_analysis.html (interactive)")
    print("   - pink_morsels_sales_analysis.png (static)")
    
    # Print some key insights
    print(f"\n📈 KEY INSIGHTS:")
    
    # Calculate average sales before and after price increase
    before_price_increase = daily_sales[daily_sales['date'] < price_change_date]['sales'].mean()
    after_price_increase = daily_sales[daily_sales['date'] >= price_change_date]['sales'].mean()
    
    print(f"   Average daily sales before price increase: ${before_price_increase:,.0f}")
    print(f"   Average daily sales after price increase: ${after_price_increase:,.0f}")
    
    sales_change = ((after_price_increase - before_price_increase) / before_price_increase) * 100
    print(f"   Sales change: {sales_change:+.1f}%")
    
    # Price increase percentage
    price_increase = ((5.0 - 3.0) / 3.0) * 100
    print(f"   Price increase: +{price_increase:.1f}%")
    
    return fig

if __name__ == "__main__":
    create_sales_visualization() 