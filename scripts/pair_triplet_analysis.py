import os
import pandas as pd
from itertools import combinations
from collections import Counter

PROCESSED_DIR = "data/processed"
CLEANED_FILENAME = "lottomax_cleaned.csv"

def pair_triplet_analysis(input_path):
    df = pd.read_csv(input_path)
    main_cols = ['n1', 'n2', 'n3', 'n4', 'n5', 'n6', 'n7']
    
    pair_counter = Counter()
    triplet_counter = Counter()

    for _, row in df.iterrows():
        numbers = [row[col] for col in main_cols]
        # Pairs
        for pair in combinations(sorted(numbers), 2):
            pair_counter[pair] += 1
        # Triplets
        for triplet in combinations(sorted(numbers), 3):
            triplet_counter[triplet] += 1

    # Convert to DataFrame and sort
    pair_df = pd.DataFrame(
        [(a, b, count) for (a, b), count in pair_counter.items()],
        columns=['num1', 'num2', 'count']
    ).sort_values(['count', 'num1', 'num2'], ascending=[False, True, True])
    
    triplet_df = pd.DataFrame(
        [(a, b, c, count) for (a, b, c), count in triplet_counter.items()],
        columns=['num1', 'num2', 'num3', 'count']
    ).sort_values(['count', 'num1', 'num2', 'num3'], ascending=[False, True, True, True])
    
    # Save to CSV
    pair_df.to_csv(os.path.join(PROCESSED_DIR, "pair_frequencies.csv"), index=False)
    triplet_df.to_csv(os.path.join(PROCESSED_DIR, "triplet_frequencies.csv"), index=False)
    
    print("Top 10 pairs:")
    print(pair_df.head(10).to_string(index=False))
    print("\nTop 10 triplets:")
    print(triplet_df.head(10).to_string(index=False))
    print("\nPair and triplet frequency tables saved to data/processed/")
    return pair_df, triplet_df

def best_pair_and_triplet_for_number(pair_df, triplet_df, number):
    # Find all pairs containing the number
    pairs_with_number = pair_df[(pair_df['num1'] == number) | (pair_df['num2'] == number)]
    if not pairs_with_number.empty:
        best_pair = pairs_with_number.iloc[0]
        print(f"\nMost frequent pair with {number}: ({best_pair['num1']}, {best_pair['num2']}) - {best_pair['count']} times")
    else:
        print(f"\nNo pairs found with {number}.")
    
    # Find all triplets containing the number
    triplets_with_number = triplet_df[
        (triplet_df['num1'] == number) | 
        (triplet_df['num2'] == number) | 
        (triplet_df['num3'] == number)
    ]
    if not triplets_with_number.empty:
        best_triplet = triplets_with_number.iloc[0]
        print(f"Most frequent triplet with {number}: ({best_triplet['num1']}, {best_triplet['num2']}, {best_triplet['num3']}) - {best_triplet['count']} times")
    else:
        print(f"No triplets found with {number}.")

def show_all_pairs_and_triplets_for_number(pair_df, triplet_df, number):
    # All pairs with the number
    pairs_with_number = pair_df[(pair_df['num1'] == number) | (pair_df['num2'] == number)]
    if not pairs_with_number.empty:
        print(f"\nAll pairs with {number} (sorted by frequency):")
        print(pairs_with_number.to_string(index=False))
    else:
        print(f"\nNo pairs found with {number}.")

    # All triplets with the number
    triplets_with_number = triplet_df[
        (triplet_df['num1'] == number) | 
        (triplet_df['num2'] == number) | 
        (triplet_df['num3'] == number)
    ]
    if not triplets_with_number.empty:
        print(f"\nAll triplets with {number} (sorted by frequency):")
        print(triplets_with_number.to_string(index=False))
    else:
        print(f"\nNo triplets found with {number}.")

if __name__ == "__main__":
    input_path = os.path.join(PROCESSED_DIR, CLEANED_FILENAME)
    pair_df, triplet_df = pair_triplet_analysis(input_path)

    while True:
        print("\nChoose an option:")
        print("1. Find best pair and triplet for a number")
        print("2. Show all pairs and triplets for a number")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == "1":
            user_input = input("Enter a number: ").strip()
            if user_input.isdigit():
                number = int(user_input)
                best_pair_and_triplet_for_number(pair_df, triplet_df, number)
            else:
                print("Please enter a valid integer.")
        elif choice == "2":
            user_input = input("Enter a number: ").strip()
            if user_input.isdigit():
                number = int(user_input)
                show_all_pairs_and_triplets_for_number(pair_df, triplet_df, number)
            else:
                print("Please enter a valid integer.")
        elif choice == "3":
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")