import pandas as pd
import numpy as np
import traceback
import warnings
import sys
from pathlib import Path

warnings.filterwarnings("ignore")

# =====================================
# FILE PATHS
# =====================================

INPUT_FILE = (
    "data/cache/parquet/"
    "growth_scored.parquet"
)

CSV_OUTPUT = (
    "data/scored/"
    "quality_scored.csv"
)

PARQUET_OUTPUT = (
    "data/cache/parquet/"
    "quality_scored.parquet"
)


# =====================================
# QUALITY SCORE
# =====================================

def calculate_quality_score(row):

    score = 0

    try:

        roe = row.get(
            "ROE",
            0
        )

        debt_to_equity = row.get(
            "DEBT_TO_EQUITY",
            0
        )

        operating_margin = row.get(
            "OPERATING_MARGIN",
            0
        )

        profit_margin = row.get(
            "PROFIT_MARGIN",
            0
        )

        pe_ratio = row.get(
            "PE_RATIO",
            0
        )

        # ---------------------------------
        # ROE
        # ---------------------------------

        if roe > 0.25:
            score += 25

        elif roe > 0.18:
            score += 18

        elif roe > 0.10:
            score += 10

        # ---------------------------------
        # DEBT
        # ---------------------------------

        if debt_to_equity < 0.30:
            score += 25

        elif debt_to_equity < 0.60:
            score += 18

        elif debt_to_equity < 1:
            score += 10

        # ---------------------------------
        # OPERATING MARGIN
        # ---------------------------------

        if operating_margin > 0.25:
            score += 20

        elif operating_margin > 0.15:
            score += 12

        elif operating_margin > 0:
            score += 5

        # ---------------------------------
        # PROFIT MARGIN
        # ---------------------------------

        if profit_margin > 0.20:
            score += 15

        elif profit_margin > 0.10:
            score += 10

        elif profit_margin > 0:
            score += 5

        # ---------------------------------
        # PE RATIO
        # ---------------------------------

        if pe_ratio > 0:

            if pe_ratio < 20:
                score += 15

            elif pe_ratio < 35:
                score += 8

    except Exception:

        return 0

    return score


# =====================================
# MAIN
# =====================================

def main():

    print("=" * 60)

    print(
        "QUALITY SCORING ENGINE"
    )

    print("=" * 60)

    # ---------------------------------
    # LOAD DATA
    # ---------------------------------

    try:

        print(
            "\nLoading parquet data..."
        )

        df = pd.read_parquet(
            INPUT_FILE
        )

    except Exception as e:

        print(
            f"ERROR loading parquet: "
            f"{e}"
        )

        traceback.print_exc()

        sys.exit(1)

    if df.empty:

        print(
            "ERROR: Empty dataset"
        )

        sys.exit(1)

    print(
        f"\nLoaded {len(df)} rows"
    )

    # ---------------------------------
    # CLEAN DATA
    # ---------------------------------

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    df = df.fillna(0)

    # ---------------------------------
    # CALCULATE QUALITY SCORE
    # ---------------------------------

    print(
        "\nCalculating quality scores..."
    )

    df["QUALITY_SCORE"] = df.apply(
        calculate_quality_score,
        axis=1
    )

    # ---------------------------------
    # SORT
    # ---------------------------------

    df = df.sort_values(
        by="QUALITY_SCORE",
        ascending=False
    )

    # ---------------------------------
    # CREATE OUTPUT DIRS
    # ---------------------------------

    Path(
        "data/scored"
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

    # ---------------------------------
    # SAVE OUTPUTS
    # ---------------------------------

    try:

        df.to_csv(
            CSV_OUTPUT,
            index=False
        )

        df.to_parquet(
            PARQUET_OUTPUT,
            index=False
        )

    except Exception as e:

        print(
            f"ERROR saving outputs: "
            f"{e}"
        )

        traceback.print_exc()

        sys.exit(1)

    # ---------------------------------
    # SUMMARY
    # ---------------------------------

    print("\n" + "=" * 60)

    print(
        "QUALITY SCORING COMPLETE"
    )

    print("=" * 60)

    print(
        f"Final Dataset Size: "
        f"{len(df)}"
    )

    print(
        f"\nTop Quality Stocks:\n"
    )

    print(
        df[
            [
                "SYMBOL",
                "QUALITY_SCORE",
                "MARKET_CAP_CATEGORY"
            ]
        ].head(20)
    )


# =====================================
# ENTRY
# =====================================

if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print(
            "\nFATAL QUALITY ENGINE ERROR"
        )

        print(str(e))

        traceback.print_exc()

        sys.exit(1)
