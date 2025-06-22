import os
import pandas as pd
import numpy as np
from scipy.stats import chisquare
from scipy.stats import norm

PROCESSED_DIR = "data/processed"
CLEANED_FILENAME = "lottomax_cleaned.csv"

def chi_square_test(input_path):
    df = pd.read_csv(input_path)
    main_cols = ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']
    all_numbers = df[main_cols].to_numpy().flatten()
    all_numbers = pd.Series(all_numbers)
    
    # Count occurrences of each number (1-50)
    observed = all_numbers.value_counts().sort_index()
    # Fill in missing numbers with 0
    for n in range(1, 51):
        if n not in observed.index:
            observed.loc[n] = 0
    observed = observed.sort_index()
    
    # Expected frequency: each number should appear equally often
    total_draws = len(df)
    expected = [total_draws * 7 / 50] * 50  # 7 numbers per draw, 50 possible numbers
    
    # Chi-square test
    chi2_stat, p_value = chisquare(f_obs=observed.values, f_exp=expected)
    
    print("Chi-square test for main numbers:")
    print(f"Chi2 statistic: {chi2_stat:.2f}")
    print(f"p-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Result: No significant deviation from randomness (fail to reject H0).")
    else:
        print("Result: Significant deviation from randomness (reject H0).")


def runs_test(input_path):
    df = pd.read_csv(input_path)
    main_cols = ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']
    all_numbers = df[main_cols].to_numpy().flatten()
    all_numbers = pd.Series(all_numbers)

    # Convert numbers to 'L' (low: 1-25) and 'H' (high: 26-50)
    hl_seq = all_numbers.apply(lambda x: 'L' if x <= 25 else 'H').tolist()

    # Count runs
    runs = 1
    for i in range(1, len(hl_seq)):
        if hl_seq[i] != hl_seq[i-1]:
            runs += 1

    n_L = hl_seq.count('L')
    n_H = hl_seq.count('H')

    # Expected number of runs
    expected_runs = ((2 * n_L * n_H) / (n_L + n_H)) + 1
    # Standard deviation
    std_runs = ((2 * n_L * n_H) * (2 * n_L * n_H - n_L - n_H)) / \
               (((n_L + n_H) ** 2) * (n_L + n_H - 1))
    std_runs = std_runs ** 0.5

    # Z-score
    z = (runs - expected_runs) / std_runs if std_runs > 0 else 0
    p_value = 2 * (1 - norm.cdf(abs(z)))

    print("Runs test for high/low sequence:")
    print(f"Number of runs: {runs}")
    print(f"Expected runs: {expected_runs:.2f}")
    print(f"Z-score: {z:.2f}")
    print(f"p-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Result: No significant deviation from randomness (fail to reject H0).")
    else:
        print("Result: Significant deviation from randomness (reject H0).")


def serial_correlation_test(input_path):
    df = pd.read_csv(input_path)
    main_cols = ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']
    all_numbers = df[main_cols].to_numpy().flatten()
    all_numbers = pd.Series(all_numbers)
    # Shift by 1 to compare each number to the next
    x = all_numbers[:-1]
    y = all_numbers[1:]
    corr = x.reset_index(drop=True).corr(y.reset_index(drop=True))
    print("Serial correlation test (lag-1):")
    print(f"Correlation coefficient: {corr:.4f}")
    if abs(corr) < 0.05:
        print("Result: No significant serial correlation (consistent with randomness).")
    else:
        print("Result: Significant serial correlation (possible non-randomness).")


def entropy_test(input_path):
    df = pd.read_csv(input_path)
    main_cols = ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']
    all_numbers = df[main_cols].to_numpy().flatten()
    all_numbers = pd.Series(all_numbers)
    freq = all_numbers.value_counts(normalize=True)
    entropy = -np.sum(freq * np.log2(freq))
    max_entropy = np.log2(50)
    print("Shannon entropy test:")
    print(f"Observed entropy: {entropy:.4f}")
    print(f"Maximum possible entropy: {max_entropy:.4f}")
    print(f"Relative entropy: {entropy / max_entropy * 100:.2f}%")
    if abs(entropy - max_entropy) < 0.1:
        print("Result: Entropy is close to maximum (consistent with randomness).")
    else:
        print("Result: Entropy is lower than expected (possible non-randomness).")

if __name__ == "__main__":
    input_path = os.path.join(PROCESSED_DIR, CLEANED_FILENAME)
    while True:
        print("\nChoose a randomness test:")
        print("1. Chi-square test")
        print("2. Runs test (high/low)")
        print("3. Serial correlation test")
        print("4. Entropy test")
        print("5. Exit")
        choice = input("Enter your choice (1/2/3/4/5): ").strip()
        if choice == "1":
            chi_square_test(input_path)
        elif choice == "2":
            runs_test(input_path)
        elif choice == "3":
            serial_correlation_test(input_path)
        elif choice == "4":
            entropy_test(input_path)
        elif choice == "5":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")