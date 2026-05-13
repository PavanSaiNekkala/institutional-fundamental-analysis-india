import pandas as pd
import numpy as np
from pathlib import Path
import traceback

INPUT_FILE = "data/raw/fundamentals.csv"
OUTPUT_FILE = "data/cleaned/cleaned_fundamentals.csv"


def clean_fundamentals():

    print("Loading raw fundamentals...")

    input_path = Path(INPUT_FILE)

    # ---------------------------------------------------
    # FILE EXISTS CHECK
    # ---------------------------------------------------
    if not input_path.exists():
        print(f"ERROR: Input file not found -> {INPUT_FILE}")
        return

    # ---------------------------------------------------
    # EMPTY FILE CHECK
    # ---------------------------------------------------
    if input_path.stat().st_size == 0:
        print("ERROR: Input CSV is empty")
        return

    try:
        df = pd.read_csv(INPUT_FILE)

    except pd.errors.EmptyDataError:
        print("ERROR: CSV contains no data")
        return

    except Exception as e:
        print("ERROR reading CSV")
        print(str(e))
        traceback.print_exc()
        return

    # ---------------------------------------------------
    # EMPTY DATAFRAME CHECK
    # ---------------------------------------------------
    if df.empty:
        print("ERROR: DataFrame is empty")
        return

    print(f"Loaded {len(df)} rows")

    # ---------------------------------------------------
    # CLEANING
    # ---------------------------------------------------
    df = df.replace([np.inf, -np.inf], np.nan)

    df = df.fillna(0)

    # Remove duplicate stocks
    if "symbol" in df.columns:
        df = df.drop_duplicates(subset=["symbol"])

    # Convert numeric columns safely
    for col in df.columns:

        try:
            df[col] = pd.to_numeric(df[col], errors="ignore")

        except Exception:
            pass

    # ---------------------------------------------------
    # SAVE
    # ---------------------------------------------------
    output_path = Path(OUTPUT_FILE)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Cleaned data saved -> {OUTPUT_FILE}")
    print(f"Final rows: {len(df)}")


if __name__ == "__main__":

    try:
        clean_fundamentals()

    except Exception as e:
        print("CLEANER FAILED")
        print(str(e))
        traceback.print_exc()
