import pandas as pd
import numpy as np
from pathlib import Path
import traceback
import warnings
import sys

warnings.filterwarnings("ignore")

INPUT_FILE = "data/financials/fundamentals.csv"
OUTPUT_FILE = "data/cleaned/cleaned_fundamentals.csv"


def clean_fundamentals():

    print("=" * 60)
    print("LOADING RAW FUNDAMENTALS")
    print("=" * 60)

    input_path = Path(INPUT_FILE)

    # ---------------------------------------------------
    # CHECK INPUT FILE EXISTS
    # ---------------------------------------------------
    if not input_path.exists():
        print(f"ERROR: Input file not found -> {INPUT_FILE}")
        sys.exit(1)

    # ---------------------------------------------------
    # CHECK FILE IS NOT EMPTY
    # ---------------------------------------------------
    if input_path.stat().st_size == 0:
        print("ERROR: Input CSV file is empty")
        sys.exit(1)

    # ---------------------------------------------------
    # READ CSV SAFELY
    # ---------------------------------------------------
    try:
        df = pd.read_csv(INPUT_FILE)

    except pd.errors.EmptyDataError:
        print("ERROR: CSV contains no rows/columns")
        sys.exit(1)

    except Exception as e:
        print("ERROR reading CSV file")
        print(str(e))
        traceback.print_exc()
        sys.exit(1)

    # ---------------------------------------------------
    # CHECK DATAFRAME
    # ---------------------------------------------------
    if df.empty:
        print("ERROR: DataFrame is empty")
        sys.exit(1)

    print(f"SUCCESS: Loaded {len(df)} rows")
    print(f"Columns Found: {len(df.columns)}")

    # ---------------------------------------------------
    # DEBUG PREVIEW
    # ---------------------------------------------------
    print("\nFIRST 5 ROWS:")
    print(df.head())

    print("\nCOLUMN NAMES:")
    print(df.columns.tolist())

    # ---------------------------------------------------
    # CLEANING PROCESS
    # ---------------------------------------------------
    print("\nCleaning data...")

    # Replace infinities
    df = df.replace([np.inf, -np.inf], np.nan)

    # Fill missing values
    df = df.fillna(0)

    # Strip spaces from column names
    df.columns = [col.strip() for col in df.columns]

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove duplicate symbols if symbol column exists
    if "symbol" in df.columns:
        df = df.drop_duplicates(subset=["symbol"])

    # ---------------------------------------------------
    # SAFE TYPE CONVERSION
    # ---------------------------------------------------
    for col in df.columns:

        try:
            # Skip symbol/text columns
            if col.lower() not in ["symbol", "sector", "industry", "company"]:
                df[col] = pd.to_numeric(df[col], errors="ignore")

        except Exception as e:
            print(f"Warning: Could not convert column -> {col}")
            print(str(e))

    # ---------------------------------------------------
    # CREATE OUTPUT DIRECTORY
    # ---------------------------------------------------
    output_path = Path(OUTPUT_FILE)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------
    # FINAL CHECK
    # ---------------------------------------------------
    if df.empty:
        print("ERROR: DataFrame became empty after cleaning")
        sys.exit(1)

    # ---------------------------------------------------
    # SAVE CLEANED DATA
    # ---------------------------------------------------
    try:

        df.to_csv(OUTPUT_FILE, index=False)

        print("\n" + "=" * 60)
        print("CLEANING COMPLETED SUCCESSFULLY")
        print("=" * 60)

        print(f"Output File : {OUTPUT_FILE}")
        print(f"Final Rows  : {len(df)}")
        print(f"Final Cols  : {len(df.columns)}")

    except Exception as e:

        print("ERROR saving cleaned CSV")
        print(str(e))
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":

    try:
        clean_fundamentals()

    except Exception as e:

        print("\nFATAL ERROR IN CLEANER")
        print(str(e))
        traceback.print_exc()

        sys.exit(1)
