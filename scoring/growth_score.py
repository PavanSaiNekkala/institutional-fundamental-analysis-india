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
    "cleaned_fundamentals.parquet"
)

OUTPUT_CSV = (
    "data/scored/"
    "growth_scored.csv"
)

OUTPUT_PARQUET = (
    "data/cache/parquet/"
    "growth_scored.parquet"
)

# =====================================================
# LOAD DATA
# =====================================================

def load_dataset():

    try:

        if not os.path.exists(INPUT_FILE):

            print(
                f"ERROR: Missing -> "
                f"{INPUT_FILE}"
            )

            sys.exit(1)

        print(
            "\nLoading cleaned fundamentals..."
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
# SAFE NUMERIC CONVERSION
# =====================================================

def safe_numeric(df, columns):

    for col in columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    return df

# =====================================================
# PERCENTILE SCORING
# =====================================================

def percentile_score(series):

    return (

        series.rank(
            pct=True
        ) * 100

    ).round(2)

# =====================================================
# GROWTH SCORING
# =====================================================

def calculate_growth_score(df):

    # ==============================================
    # REQUIRED COLUMNS
    # ==============================================

    growth_columns = [

        "REVENUE_GROWTH",
        "EARNINGS_GROWTH",
        "ROE",
        "OPERATING_MARGIN"

    ]

    df = safe_numeric(
        df,
        growth_columns
    )

    # ==============================================
    # CLEAN NEGATIVE EXTREMES
    # ==============================================

    for col in growth_columns:

        if col in df.columns:

            lower = df[col].quantile(0.01)

            upper = df[col].quantile(0.99)

            df[col] = np.clip(
                df[col],
                lower,
                upper
            )

    # ==============================================
    # PERCENTILE SCORES
    # ==============================================

    df["REVENUE_GROWTH_SCORE"] = (

        percentile_score(
            df["REVENUE_GROWTH"]
        )

    )

    df["EARNINGS_GROWTH_SCORE"] = (

        percentile_score(
            df["EARNINGS_GROWTH"]
        )

    )

    df["ROE_SCORE"] = (

        percentile_score(
            df["ROE"]
        )

    )

    df["OPERATING_MARGIN_SCORE"] = (

        percentile_score(
            df["OPERATING_MARGIN"]
        )

    )

    # ==============================================
    # GROWTH STABILITY
    # ==============================================

    df["GROWTH_STABILITY_SCORE"] = (

        (
            df["REVENUE_GROWTH_SCORE"]
            +
            df["EARNINGS_GROWTH_SCORE"]
        ) / 2

    )

    # ==============================================
    # FINAL GROWTH SCORE
    # ==============================================

    df["GROWTH_SCORE"] = (

        (
            df["REVENUE_GROWTH_SCORE"]
            * 0.35
        )

        +

        (
            df["EARNINGS_GROWTH_SCORE"]
            * 0.35
        )

        +

        (
            df["ROE_SCORE"]
            * 0.20
        )

        +

        (
            df["OPERATING_MARGIN_SCORE"]
            * 0.10
        )

    ).round(2)

    return df

# =====================================================
# GROWTH CATEGORY
# =====================================================

def assign_growth_category(score):

    if score >= 85:

        return "ELITE GROWTH"

    elif score >= 70:

        return "HIGH GROWTH"

    elif score >= 55:

        return "MODERATE GROWTH"

    elif score >= 40:

        return "SLOW GROWTH"

    return "WEAK GROWTH"

# =====================================================
# MAIN PIPELINE
# =====================================================

def main():

    print("=" * 60)

    print(
        "INSTITUTIONAL GROWTH "
        "SCORING ENGINE"
    )

    print("=" * 60)

    # =================================================
    # LOAD DATA
    # =================================================

    df = load_dataset()

    # =================================================
    # CALCULATE SCORES
    # =================================================

    df = calculate_growth_score(df)

    # =================================================
    # GROWTH CATEGORY
    # =================================================

    df["GROWTH_CATEGORY"] = (

        df["GROWTH_SCORE"]

        .apply(assign_growth_category)

    )

    # =================================================
    # FINAL SORT
    # =================================================

    df = df.sort_values(

        by="GROWTH_SCORE",

        ascending=False
    )

    # =================================================
    # CREATE OUTPUT DIRS
    # =================================================

    os.makedirs(
        "data/scored",
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
        "GROWTH SCORING COMPLETE"
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

    print(
        "\nGrowth Category Distribution:\n"
    )

    print(
        df["GROWTH_CATEGORY"]
        .value_counts()
    )

    print("\nTop Growth Stocks:\n")

    print(

        df[
            [
                "SYMBOL",
                "GROWTH_SCORE",
                "GROWTH_CATEGORY"
            ]
        ]

        .head(15)

    )

# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print(
            "\nFATAL GROWTH SCORING ERROR"
        )

        print(str(e))

        traceback.print_exc()

        sys.exit(1)
