import pandas as pd

def analyze_price_changes():
    """Analyze price changes across all three data files"""
    
    files = [
        'data/daily_sales_data_0.csv',
        'data/daily_sales_data_1.csv', 
        'data/daily_sales_data_2.csv'
    ]
    
    all_pink_data = []
    
    for i, file in enumerate(files):
        print(f"Analyzing File {i}: {file}")
        df = pd.read_csv(file)
        pink = df[df['product'].str.lower() == 'pink morsel'].copy()
        
        # Clean price and convert to float
        pink['price'] = pink['price'].str.replace('$', '').astype(float)
        
        print(f"  Date range: {pink['date'].min()} to {pink['date'].max()}")
        print(f"  Unique prices: {pink['price'].unique()}")
        print(f"  Records: {len(pink)}")
        
        # Group by price to see when changes occurred
        price_summary = pink.groupby('price').agg({
            'date': ['min', 'max', 'count']
        }).round(2)
        print(f"  Price summary:")
        print(price_summary)
        print()
        
        all_pink_data.append(pink)
    
    # Combine all data
    combined = pd.concat(all_pink_data, ignore_index=True)
    combined['date'] = pd.to_datetime(combined['date'])
    combined = combined.sort_values('date')
    
    print("=== OVERALL ANALYSIS ===")
    print(f"Total date range: {combined['date'].min().date()} to {combined['date'].max().date()}")
    print(f"Unique prices: {sorted(combined['price'].unique())}")
    
    # Find price change points
    price_changes = combined.groupby('price').agg({
        'date': ['min', 'max']
    }).round(2)
    print(f"\nPrice change timeline:")
    print(price_changes)
    
    # Check for any price increases
    unique_prices = sorted(combined['price'].unique())
    if len(unique_prices) > 1:
        print(f"\n💰 PRICE INCREASES DETECTED:")
        for i in range(len(unique_prices) - 1):
            old_price = unique_prices[i]
            new_price = unique_prices[i + 1]
            increase = ((new_price - old_price) / old_price) * 100
            print(f"  {old_price} → {new_price} (+{increase:.1f}%)")
    else:
        print(f"\n📊 No price changes detected - price remained at ${unique_prices[0]}")
    
    return combined

if __name__ == "__main__":
    analyze_price_changes() 