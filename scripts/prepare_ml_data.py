import os
import pandas as pd
import numpy as np

PROCESSED_DIR = "data/processed"
CLEANED_FILENAME = "lottomax_cleaned.csv"
ML_FILENAME = "lottomax_ml_ready.csv"

def prepare_ml_data():
    path = os.path.join(PROCESSED_DIR, CLEANED_FILENAME)
    df = pd.read_csv(path)
    main_cols = ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']
    
    # Create a binary matrix: rows = draws, columns = numbers 1-50
    ml_matrix = np.zeros((len(df), 50), dtype=int)
    for i, row in df.iterrows():
        for n in row[main_cols]:
            ml_matrix[i, int(n)-1] = 1  # -1 for zero-based index
    
    ml_df = pd.DataFrame(ml_matrix, columns=[f"num_{i}" for i in range(1, 51)])
    ml_df['draw_date'] = df['draw_date']
    ml_df['bonus'] = df['bonus']
    
    # Save for ML use
    ml_df.to_csv(os.path.join(PROCESSED_DIR, ML_FILENAME), index=False)
    print(f"ML-ready data saved to {os.path.join(PROCESSED_DIR, ML_FILENAME)}")

if __name__ == "__main__":
    prepare_ml_data()