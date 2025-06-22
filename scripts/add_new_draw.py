import os
import sys
import pandas as pd

PROCESSED_DIR = "data/processed"
CLEANED_FILENAME = "lottomax_cleaned.csv"

def show_last_draw(df):
    if 'draw_date' not in df.columns or df.empty:
        print("No draw data found.")
        return
    df['draw_date'] = pd.to_datetime(df['draw_date'])
    last_row = df.sort_values('draw_date').iloc[-1]
    print(f"\nLast draw date: {last_row['draw_date'].date()}")
    numbers = [int(x) for x in last_row[['n1','n2','n3','n4','n5','n6','n7']]]
    print(f"Numbers: {numbers}")
    print(f"Bonus: {int(last_row['bonus'])}\n")


def add_new_draw():
    # Load existing data
    path = os.path.join(PROCESSED_DIR, CLEANED_FILENAME)
    df = pd.read_csv(path)
    
    # Show last draw info
    show_last_draw(df)

    # Prompt for date
    draw_date = input("Enter draw date (YYYY-MM-DD) or press Enter to exit: ").strip()
    if not draw_date:
        print("No input provided. Exiting.")
        sys.exit(1)
    if draw_date in df['draw_date'].values:
        print(f"Draw for {draw_date} already exists. Exiting.")
        sys.exit(1)
    
    # Prompt for numbers
    numbers_str = input("Enter 7 main numbers separated by commas (e.g. 5,12,23,34,41,44,49) or press Enter to exit: ").strip()
    if not numbers_str:
        print("No input provided. Exiting.")
        sys.exit(1)
    try:
        numbers = [int(n) for n in numbers_str.split(',')]
    except ValueError:
        print("Invalid input. Please enter 7 integers separated by commas. Exiting.")
        sys.exit(1)
    if len(numbers) != 7 or not all(1 <= n <= 50 for n in numbers):
        print("You must provide exactly 7 numbers between 1 and 50. Exiting.")
        sys.exit(1)
    
    # Prompt for bonus number
    bonus_str = input("Enter bonus number (1-50) or press Enter to exit: ").strip()
    if not bonus_str:
        print("No input provided. Exiting.")
        sys.exit(1)
    try:
        bonus = int(bonus_str)
    except ValueError:
        print("Invalid input. Please enter an integer for the bonus number. Exiting.")
        sys.exit(1)
    if not (1 <= bonus <= 50):
        print("Bonus number must be between 1 and 50. Exiting.")
        sys.exit(1)
    
    # Prepare new row
    new_row = {
        'draw_date': draw_date,
        'n1': numbers[0], 'n2': numbers[1], 'n3': numbers[2], 'n4': numbers[3],
        'n5': numbers[4], 'n6': numbers[5], 'n7': numbers[6],
        'bonus': bonus
    }
    
    # Append and sort
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df['draw_date'] = pd.to_datetime(df['draw_date'])
    df = df.sort_values('draw_date')
    
    # Save back
    df.to_csv(path, index=False)
    print(f"Draw for {draw_date} added successfully.")

if __name__ == "__main__":
    add_new_draw()