import pandas as pd
import os


INPUT_FILE = "data/financials/fundamentals.csv"
OUTPUT_FILE = "data/cleaned/cleaned_fundamentals.csv"


def clean_fundamentals():

    print("Loading raw fundamentals...")

    df = pd.read_csv(INPUT_FILE)

    print(f"Initial Rows: {len(df)}")

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Fill missing numeric values
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns

    for col in numeric_cols:
        df[col] = df[col].fillna(0)

    # Standardize column names
    df.columns = [col.upper() for col in df.columns]

    # Remove rows with missing symbols
    df = df[df["SYMBOL"].notna()]

    print(f"Cleaned Rows: {len(df)}")

    os.makedirs("data/cleaned", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nCleaned data saved to: {OUTPUT_FILE}")

    return df


if __name__ == "__main__":

    clean_fundamentals()
  
