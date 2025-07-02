import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

PROCESSED_DIR = "data/processed"
ML_FILENAME = "lottomax_ml_ready.csv"

def make_lagged_features(df, num_cols, n_lags=3):
    # Create lagged features for each previous draw
    lagged_features = []
    for lag in range(1, n_lags+1):
        lagged = df[num_cols].shift(lag)
        lagged.columns = [f"{col}_lag{lag}" for col in num_cols]
        lagged_features.append(lagged)
    X = pd.concat(lagged_features, axis=1).iloc[n_lags:]
    y = df[num_cols].iloc[n_lags:]
    return X.values, y.values

def main(n_lags=3):
    path = os.path.join(PROCESSED_DIR, ML_FILENAME)
    df = pd.read_csv(path)
    num_cols = [f"num_{i}" for i in range(1, 51)]
    
    X, y = make_lagged_features(df, num_cols, n_lags=n_lags)
    
    # Train/test split (last 20 draws as test)
    split_idx = -20
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
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
            auc = np.nan
        accs.append(acc)
        aucs.append(auc)
        print(f"{col}: Accuracy={acc:.3f}, ROC-AUC={auc if not np.isnan(auc) else 'N/A'}")
    
    print(f"\nAverage accuracy across all numbers: {np.mean(accs):.3f}")
    print(f"Average ROC-AUC across all numbers: {np.nanmean(aucs):.3f}")

if __name__ == "__main__":
    # Change n_lags to use more or fewer previous draws
    main(n_lags=54)