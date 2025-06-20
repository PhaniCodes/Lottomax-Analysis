import os
import pandas as pd

PROCESSED_DIR = "data/processed"
CLEANED_FILENAME = "lottomax_cleaned.csv"

def frequency_analysis(input_path):
    df = pd.read_csv(input_path)
    
    # Main numbers columns
    main_cols = ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']
    bonus_col = 'bonus'

    # Flatten all main numbers into a single series
    main_numbers = pd.concat([df[col] for col in main_cols])
    main_freq = main_numbers.value_counts().reset_index()
    main_freq.columns = ['number', 'count']
    main_freq = main_freq.sort_values(['count', 'number'], ascending=[False, True]).set_index('number')
    
    # Bonus number frequency (if present and not all missing)
    if bonus_col in df.columns and df[bonus_col].notna().any():
        bonus_numbers = df[bonus_col].dropna()
        bonus_freq = bonus_numbers.value_counts().reset_index()
        bonus_freq.columns = ['number', 'count']
        bonus_freq = bonus_freq.sort_values(['count', 'number'], ascending=[False, True]).set_index('number')
    else:
        bonus_numbers = pd.Series(dtype=int)
        bonus_freq = pd.DataFrame(columns=['count'])

    # Combined (main + bonus)
    all_numbers = pd.concat([main_numbers, bonus_numbers])
    all_freq = all_numbers.value_counts().reset_index()
    all_freq.columns = ['number', 'count']
    all_freq = all_freq.sort_values(['count', 'number'], ascending=[False, True]).set_index('number')
    
    print("Main Number Frequencies (Descending order):")
    print(main_freq)
    print("\nBonus Number Frequencies (Descending Order):")
    print(bonus_freq)
    print ("\nCombined (Main + Bonus) Number Frequencies (Descending Order):")
    print(all_freq)
    
    # save to CSV
    main_freq.to_csv(os.path.join(PROCESSED_DIR, "main_number_frequencies.csv"), header=["count"])
    bonus_freq.to_csv(os.path.join(PROCESSED_DIR, "bonus_number_frequencies.csv"), header=["count"])
    print("\nFrequency tables saved to data/processed/")

if __name__ == "__main__":
    input_path = os.path.join(PROCESSED_DIR, CLEANED_FILENAME)
    frequency_analysis(input_path)