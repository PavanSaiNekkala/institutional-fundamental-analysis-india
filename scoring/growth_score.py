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

PARQUET_INPUT = (
    "data/cache/parquet/"
    "cleaned_fundamentals.parquet"
)

CSV_OUTPUT = (
    "data/scored/"
    "growth_scored.csv"
)

PARQUET_OUTPUT = (
    "data/cache/parquet/"
    "growth_scored.parquet"
)

# =====================================
# GROWTH SCORE FUNCTION
# =====================================

def calculate_growth_score(row):

    score = 0

    try:

        revenue_growth = row.get(
            "REVENUE_GROWTH",
            0
        )

        earnings_growth = row.get(
            "EARNINGS_GROWTH",
            0
        )

        roe = row.get(
            "ROE",
            0
        )

        operating_margin = row.get(
            "OPERATING_MARGIN",
            0
        )

        # ---------------------------------
        # REVENUE GROWTH
        # ---------------------------------

        if revenue_growth > 0.30:
            score += 30

        elif revenue_growth > 0.20:
            score += 20

        elif revenue_growth > 0.10:
            score += 10

        # ---------------------------------
        # EARNINGS GROWTH
        # ---------------------------------

        if earnings_growth > 0.30:
            score += 30

        elif earnings_growth > 0.20:
            score += 20

        elif earnings_growth > 0.10:
            score += 10

        # ---------------------------------
        # ROE
        # ---------------------------------

        if roe > 0.20:
            score += 20

        elif roe > 0.15:
            score += 10

        # ---------------------------------
        # OPERATING MARGIN
        # ---------------------------------

        if operating_margin > 0.20:
            score += 20

        elif operating_margin > 0.10:
            score += 10

    except Exception:

        return 0

    return score

# =====================================
# MAIN
# =====================================

def main():

    print("=" * 60)

    print(
        "GROWTH SCORING ENGINE"
    )

    print("=" * 60)

    # ---------------------------------
    # FILE CHECK
    # ---------------------------------

    input_path = Path(
        PARQUET_INPUT
    )

    if not input_path.exists():

        print(
            f"ERROR: Missing input parquet -> "
            f"{PARQUET_INPUT}"
        )

        sys.exit(1)

    # ---------------------------------
    # LOAD DATA
    # ---------------------------------

    try:

        print(
            "\nLoading parquet data..."
        )

        df = pd.read_parquet(
            PARQUET_INPUT
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
    # CALCULATE GROWTH SCORE
    # ---------------------------------

    print(
        "\nCalculating growth scores..."
    )

    df["GROWTH_SCORE"] = df.apply(
        calculate_growth_score,
        axis=1
    )

    # ---------------------------------
    # SORT
    # ---------------------------------

    df = df.sort_values(
        by="GROWTH_SCORE",
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
        "GROWTH SCORING COMPLETE"
    )

    print("=" * 60)

    print(
        f"Final Dataset Size: "
        f"{len(df)}"
    )

    print(
        f"\nParquet Saved To:\n"
        f"{PARQUET_OUTPUT}"
    )

# =====================================
# ENTRY
# =====================================

if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print(
            "\nFATAL GROWTH ENGINE ERROR"
        )

        print(str(e))

        traceback.print_exc()

        sys.exit(1)
