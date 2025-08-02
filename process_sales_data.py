import pandas as pd
import os

def process_sales_data():
    """
    Process the three CSV files containing Soul Foods morsel sales data.
    Filter for pink morsels only, calculate sales (price * quantity),
    and output a single formatted CSV file.
    """
    
    # List of CSV files to process
    csv_files = [
        'data/daily_sales_data_0.csv',
        'data/daily_sales_data_1.csv', 
        'data/daily_sales_data_2.csv'
    ]
    
    # List to store processed dataframes
    processed_dfs = []
    
    # Process each CSV file
    for file_path in csv_files:
        print(f"Processing {file_path}...")
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Filter for pink morsels only (case-insensitive)
        pink_morsels = df[df['product'].str.lower() == 'pink morsel'].copy()
        
        if len(pink_morsels) == 0:
            print(f"Warning: No pink morsels found in {file_path}")
            continue
        
        # Clean price column by removing '$' and converting to float
        pink_morsels['price'] = pink_morsels['price'].str.replace('$', '').astype(float)
        
        # Calculate sales (price * quantity)
        pink_morsels['sales'] = pink_morsels['price'] * pink_morsels['quantity']
        
        # Select only the required columns: sales, date, region
        final_df = pink_morsels[['sales', 'date', 'region']].copy()
        
        processed_dfs.append(final_df)
        
        print(f"  - Found {len(pink_morsels)} pink morsel records")
    
    # Combine all processed dataframes
    if processed_dfs:
        combined_df = pd.concat(processed_dfs, ignore_index=True)
        
        # Sort by date for better organization
        combined_df = combined_df.sort_values('date')
        
        # Save to output file
        output_file = 'formatted_sales_data.csv'
        combined_df.to_csv(output_file, index=False)
        
        print(f"\n✅ Processing complete!")
        print(f"📊 Total records: {len(combined_df)}")
        print(f"📅 Date range: {combined_df['date'].min()} to {combined_df['date'].max()}")
        print(f"🌍 Regions: {', '.join(combined_df['region'].unique())}")
        print(f"💰 Sales range: ${combined_df['sales'].min():.2f} to ${combined_df['sales'].max():.2f}")
        print(f"💾 Output saved to: {output_file}")
        
        # Display first few rows
        print(f"\n📋 First 5 rows of output:")
        print(combined_df.head())
        
        return combined_df
    else:
        print("❌ No data was processed. Check if pink morsels exist in the input files.")
        return None

if __name__ == "__main__":
    process_sales_data() 