import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

PROCESSED_DIR = "data/processed"
ML_FILENAME = "lottomax_ml_ready.csv"

def main():
    path = os.path.join(PROCESSED_DIR, ML_FILENAME)
    df = pd.read_csv(path)
    num_cols = [f"num_{i}" for i in range(1, 51)]
    
    # Use previous draw as features, current draw as label
    X = df[num_cols].shift(1).iloc[1:].values  # previous draw
    y = df[num_cols].iloc[1:].values           # current draw
    
    # Train/test split (simple: last 20 draws as test)
    split_idx = -20
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    # Train a model for each number
    accs = []
    aucs = []
    for i, col in enumerate(num_cols):
        model = LogisticRegression(solver='liblinear')
        model.fit(X_train, y_train[:, i])
        preds = model.predict(X_test)
        probas = model.predict_proba(X_test)[:, 1]
        acc = accuracy_score(y_test[:, i], preds)
        try:
            auc = roc_auc_score(y_test[:, i], probas)
        except ValueError:
            auc = np.nan  # If only one class in y_test
        accs.append(acc)
        aucs.append(auc)
        print(f"{col}: Accuracy={acc:.3f}, ROC-AUC={auc if not np.isnan(auc) else 'N/A'}")
    
    print(f"\nAverage accuracy across all numbers: {np.mean(accs):.3f}")
    print(f"Average ROC-AUC across all numbers: {np.nanmean(aucs):.3f}")

if __name__ == "__main__":
    main()