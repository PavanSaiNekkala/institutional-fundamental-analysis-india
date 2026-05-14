import os
import sys
import traceback
import warnings

import pandas as pd
import numpy as np

warnings.filterwarnings("ignore")

# =====================================================
# PROJECT ROOT FIX
# =====================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if PROJECT_ROOT not in sys.path:

    sys.path.insert(
        0,
        PROJECT_ROOT
    )

# =====================================================
# INPUT / OUTPUT
# =====================================================

INPUT_FILE = (
    "data/cache/parquet/"
    "fundamentals.parquet"
)

OUTPUT_CSV = (
    "data/processed/"
    "cleaned_fundamentals.csv"
)

OUTPUT_PARQUET = (
    "data/cache/parquet/"
    "cleaned_fundamentals.parquet"
)

# =====================================================
# SECTOR NORMALIZATION
# =====================================================

SECTOR_MAPPING = {

    "Financial Services":
        "Financials",

    "Banks":
        "Financials",

    "Technology":
        "Information Technology",

    "Tech":
        "Information Technology",

    "Healthcare":
        "Healthcare",

    "Consumer Cyclical":
        "Consumer",

    "Consumer Defensive":
        "Consumer",

    "Energy":
        "Energy",

    "Industrials":
        "Industrials",

    "Basic Materials":
        "Materials",

    "Utilities":
        "Utilities",

    "Real Estate":
        "Real Estate",

    "Communication Services":
        "Communication",

    "Unknown":
        "Other"
}

# =====================================================
# LOAD DATA
# =====================================================

def load_dataset():

    try:

        if not os.path.exists(INPUT_FILE):

            print(
                f"ERROR: Missing file -> "
                f"{INPUT_FILE}"
            )

            sys.exit(1)

        print(
            "\nLoading fundamentals..."
        )

        df = pd.read_parquet(INPUT_FILE)

        if df.empty:

            print(
                "ERROR: Empty dataset"
            )

            sys.exit(1)

        print(
            f"Loaded "
            f"{len(df)} rows"
        )

        return df

    except Exception as e:

        print(
            f"Load error: {e}"
        )

        traceback.print_exc()

        sys.exit(1)

# =====================================================
# STANDARDIZE SECTORS
# =====================================================

def normalize_sectors(df):

    if "SECTOR" not in df.columns:

        return df

    df["SECTOR"] = (

        df["SECTOR"]

        .fillna("Other")

        .replace(SECTOR_MAPPING)

    )

    return df

# =====================================================
# REMOVE DUPLICATES
# =====================================================

def remove_duplicates(df):

    if "SYMBOL" in df.columns:

        df = (

            df

            .sort_values(
                by="MARKET_CAP",
                ascending=False
            )

            .drop_duplicates(
                subset=["SYMBOL"]
            )
        )

    return df

# =====================================================
# VALIDATION FILTERS
# =====================================================

def apply_validation(df):

    # ---------------------------------------------
    # MARKET CAP
    # ---------------------------------------------

    if "MARKET_CAP" in df.columns:

        df = df[
            df["MARKET_CAP"] > 0
        ]

    # ---------------------------------------------
    # CURRENT PRICE
    # ---------------------------------------------

    if "CURRENT_PRICE" in df.columns:

        df = df[
            df["CURRENT_PRICE"] > 0
        ]

    # ---------------------------------------------
    # SYMBOL
    # ---------------------------------------------

    if "SYMBOL" in df.columns:

        df = df[
            df["SYMBOL"].notna()
        ]

    return df

# =====================================================
# HANDLE MISSING VALUES
# =====================================================

def handle_missing_values(df):

    numeric_columns = df.select_dtypes(
        include=[np.number]
    ).columns

    for col in numeric_columns:

        median_value = df[col].median()

        df[col] = df[col].fillna(
            median_value
        )

    categorical_columns = (

        df.select_dtypes(
            exclude=[np.number]
        ).columns

    )

    for col in categorical_columns:

        df[col] = df[col].fillna(
            "Unknown"
        )

    return df

# =====================================================
# OUTLIER CONTROL
# =====================================================

def winsorize_columns(df):

    columns = [

        "PE_RATIO",
        "ROE",
        "REVENUE_GROWTH",
        "EARNINGS_GROWTH",
        "DEBT_TO_EQUITY"

    ]

    for col in columns:

        if col in df.columns:

            lower = df[col].quantile(0.01)

            upper = df[col].quantile(0.99)

            df[col] = np.clip(
                df[col],
                lower,
                upper
            )

    return df

# =====================================================
# CREATE INSTITUTIONAL FLAGS
# =====================================================

def create_flags(df):

    # ---------------------------------------------
    # QUALITY FLAG
    # ---------------------------------------------

    df["HIGH_QUALITY_FLAG"] = np.where(

        (
            (df["ROE"] > 0.15)
            &
            (df["DEBT_TO_EQUITY"] < 1)
        ),

        1,

        0
    )

    # ---------------------------------------------
    # GROWTH FLAG
    # ---------------------------------------------

    df["HIGH_GROWTH_FLAG"] = np.where(

        (
            (df["REVENUE_GROWTH"] > 0.10)
            &
            (df["EARNINGS_GROWTH"] > 0.10)
        ),

        1,

        0
    )

    return df

# =====================================================
# MAIN PIPELINE
# =====================================================

def main():

    print("=" * 60)

    print(
        "INSTITUTIONAL CLEANING PIPELINE"
    )

    print("=" * 60)

    # =================================================
    # LOAD
    # =================================================

    df = load_dataset()

    # =================================================
    # CLEANING
    # =================================================

    df = normalize_sectors(df)

    df = remove_duplicates(df)

    df = apply_validation(df)

    df = handle_missing_values(df)

    df = winsorize_columns(df)

    df = create_flags(df)

    # =================================================
    # FINAL SORT
    # =================================================

    if "MARKET_CAP" in df.columns:

        df = df.sort_values(

            by="MARKET_CAP",

            ascending=False
        )

    # =================================================
    # CREATE DIRECTORIES
    # =================================================

    os.makedirs(
        "data/processed",
        exist_ok=True
    )

    os.makedirs(
        "data/cache/parquet",
        exist_ok=True
    )

    # =================================================
    # SAVE OUTPUTS
    # =================================================

    df.to_csv(
        OUTPUT_CSV,
        index=False
    )

    df.to_parquet(
        OUTPUT_PARQUET,
        index=False
    )

    # =================================================
    # SUMMARY
    # =================================================

    print("\n" + "=" * 60)

    print(
        "CLEANING COMPLETE"
    )

    print("=" * 60)

    print(
        f"Final Dataset Size: "
        f"{len(df)}"
    )

    print(
        f"\nCSV Saved:\n"
        f"{OUTPUT_CSV}"
    )

    print(
        f"\nParquet Saved:\n"
        f"{OUTPUT_PARQUET}"
    )

    print("\nSector Distribution:\n")

    print(
        df["SECTOR"]
        .value_counts()
        .head(15)
    )

    print("\nSample Data:\n")

    print(df.head())

# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print(
            "\nFATAL CLEANING ERROR"
        )

        print(str(e))

        traceback.print_exc()

        sys.exit(1)
