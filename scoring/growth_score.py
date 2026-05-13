import pandas as pd
import numpy as np
from pathlib import Path
import traceback
import warnings
import sys

warnings.filterwarnings("ignore")

# =====================================
# INPUT / OUTPUT
# =====================================

PARQUET_OUTPUT = (
    "data/cache/parquet/"
    "growth_scored.parquet"
)

CSV_OUTPUT = (
    "data/cleaned/"
    "cleaned_fundamentals.csv"
)

PARQUET_OUTPUT = (
    "data/cache/parquet/"
    "cleaned_fundamentals.parquet"
)


# =====================================
# CLEANER
# =====================================

def clean_fundamentals():

    print("=" * 60)

    print(
        "CLEANING INSTITUTIONAL "
        "FUNDAMENTALS"
    )

    print("=" * 60)

    input_path = Path(PARQUET_INPUT)

    # ---------------------------------
    # FILE CHECK
    # ---------------------------------

    if not input_path.exists():

        print(
            f"ERROR: Input file missing -> "
            f"{PARQUET_INPUT}"
        )

        sys.exit(1)

    # ---------------------------------
    # LOAD PARQUET
    # ---------------------------------

    try:

        print(
            "\nLoading parquet cache..."
        )

        df = pd.read_parquet(
            PARQUET_INPUT
        )

    except Exception as e:

        print(
            f"ERROR reading parquet: "
            f"{e}"
        )

        traceback.print_exc()

        sys.exit(1)

    # ---------------------------------
    # EMPTY CHECK
    # ---------------------------------

    if df.empty:

        print(
            "ERROR: DataFrame is empty"
        )

        sys.exit(1)

    print(
        f"\nLoaded {len(df)} rows"
    )

    print(
        f"Columns Found: "
        f"{len(df.columns)}"
    )

    # ---------------------------------
    # PREVIEW
    # ---------------------------------

    print("\nSample Data:\n")

    print(df.head())

    # =====================================
    # CLEANING
    # =====================================

    print("\nCleaning data...")

    # Replace inf values
    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    # Fill missing values
    df = df.fillna(0)

    # Remove duplicates
    df = df.drop_duplicates()

    # Remove duplicate symbols
    if "SYMBOL" in df.columns:

        df = df.drop_duplicates(
            subset=["SYMBOL"]
        )

    # Strip column spaces
    df.columns = [
        col.strip()
        for col in df.columns
    ]

    # =====================================
    # SAFE TYPE CONVERSION
    # =====================================

    excluded_columns = [

        "SYMBOL",
        "SECTOR",
        "RAW_SECTOR",
        "INDUSTRY",
        "FETCH_DATE",
        "MARKET_CAP_CATEGORY"
    ]

    for col in df.columns:

        try:

            if col not in excluded_columns:

                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )

        except Exception as e:

            print(
                f"Warning converting "
                f"{col}: {e}"
            )

    # Replace conversion NaNs
    df = df.fillna(0)

    # =====================================
    # OUTPUT DIRECTORIES
    # =====================================

    Path(
        "data/cleaned"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    Path(
        "data/cache/parquet"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    # =====================================
    # SAVE OUTPUTS
    # =====================================

    try:

        # CSV export
        df.to_csv(
            CSV_OUTPUT,
            index=False
        )

        # Parquet export
        df.to_parquet(
            PARQUET_OUTPUT,
            index=False
        )

    except Exception as e:

        print(
            f"ERROR saving cleaned "
            f"outputs: {e}"
        )

        traceback.print_exc()

        sys.exit(1)

    # =====================================
    # SUMMARY
    # =====================================

    print("\n" + "=" * 60)

    print(
        "DATA CLEANING COMPLETE"
    )

    print("=" * 60)

    print(
        f"Final Rows: {len(df)}"
    )

    print(
        f"Final Columns: "
        f"{len(df.columns)}"
    )

    print(
        f"\nCSV Saved To:\n"
        f"{CSV_OUTPUT}"
    )

    print(
        f"\nParquet Saved To:\n"
        f"{PARQUET_OUTPUT}"
    )


# =====================================
# ENTRY POINT
# =====================================

if __name__ == "__main__":

    try:

        clean_fundamentals()

    except Exception as e:

        print(
            "\nFATAL CLEANER ERROR"
        )

        print(str(e))

        traceback.print_exc()

        sys.exit(1)
