import os
import pandas as pd

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
RAW_FILENAME = "lottomax_history.xlsx" 
PROCESSED_FILENAME = "lottomax_cleaned.csv"

def clean_lottomax_data(input_path, output_path):
    # Read Excel file
    df = pd.read_excel(input_path)
    
    # Standardize column names
    df.columns = [col.strip().lower() for col in df.columns]
    
    # Ensure required columns exist
    required = ['draw_date', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Handle bonus column
    if 'bonus' not in df.columns:
        df['bonus'] = None
    
    # Convert draw_date to datetime and sort
    df['draw_date'] = pd.to_datetime(df['draw_date'])
    df = df.sort_values('draw_date')
    
    # Drop duplicates
    df = df.drop_duplicates(subset=['draw_date', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'bonus'])

    # Reorder columns for consistency
    output_cols = ['draw_date', 'n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7', 'bonus']
    df = df[output_cols]
    
    # Save cleaned data
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    input_path = os.path.join(RAW_DIR, RAW_FILENAME)
    output_path = os.path.join(PROCESSED_DIR, PROCESSED_FILENAME)
    clean_lottomax_data(input_path, output_path)