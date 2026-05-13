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
    "quality_scored.parquet"
)

CSV_OUTPUT = (
    "data/scored/"
    "ownership_scored.csv"
)

PARQUET_OUTPUT = (
    "data/cache/parquet/"
    "ownership_scored.parquet"
)


# =====================================
# OWNERSHIP SCORE
# =====================================

def calculate_ownership_score(row):

    score = 0

    try:

        market_cap = row.get(
            "MARKET_CAP",
            0
        )

        roe = row.get(
            "ROE",
            0
        )

        profit_margin = row.get(
            "PROFIT_MARGIN",
            0
        )

        revenue_growth = row.get(
            "REVENUE_GROWTH",
            0
        )

        debt_to_equity = row.get(
            "DEBT_TO_EQUITY",
            0
        )

        # ---------------------------------
        # MARKET CAP
        # ---------------------------------

        if market_cap > 500000000000:
            score += 30

        elif market_cap > 100000000000:
            score += 20

        elif market_cap > 10000000000:
            score += 10

        # ---------------------------------
        # ROE
        # ---------------------------------

        if roe > 0.20:
            score += 20

        elif roe > 0.15:
            score += 10

        # ---------------------------------
        # PROFITABILITY
        # ---------------------------------

        if profit_margin > 0.20:
            score += 20

        elif profit_margin > 0.10:
            score += 10

        # ---------------------------------
        # GROWTH
        # ---------------------------------

        if revenue_growth > 0.20:
            score += 20

        elif revenue_growth > 0.10:
            score += 10

        # ---------------------------------
        # LOW DEBT
        # ---------------------------------

        if debt_to_equity < 0.5:
            score += 10

        elif debt_to_equity < 1:
            score += 5

    except Exception:

        return 0

    return score


# =====================================
# MAIN
# =====================================

def main():

    print("=" * 60)

    print(
        "OWNERSHIP SCORING ENGINE"
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
    # CALCULATE SCORE
    # ---------------------------------

    print(
        "\nCalculating ownership scores..."
    )

    df["OWNERSHIP_SCORE"] = df.apply(
        calculate_ownership_score,
        axis=1
    )

    # ---------------------------------
    # SORT
    # ---------------------------------

    df = df.sort_values(
        by="OWNERSHIP_SCORE",
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
        "OWNERSHIP SCORING COMPLETE"
    )

    print("=" * 60)

    print(
        f"Final Dataset Size: "
        f"{len(df)}"
    )

    print(
        "\nTop Institutional "
        "Ownership Stocks:\n"
    )

    print(
        df[
            [
                "SYMBOL",
                "OWNERSHIP_SCORE",
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
            "\nFATAL OWNERSHIP ENGINE ERROR"
        )

        print(str(e))

        traceback.print_exc()

        sys.exit(1)
