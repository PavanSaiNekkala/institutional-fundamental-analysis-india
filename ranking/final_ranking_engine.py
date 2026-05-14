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
    "ownership_scored.parquet"
)

CSV_OUTPUT = (
    "exports/"
    "institutional_rankings.csv"
)

PARQUET_OUTPUT = (
    "data/cache/parquet/"
    "institutional_rankings.parquet"
)

# =====================================
# MARKET REGIME
# =====================================

def determine_market_regime(df):

    try:

        avg_growth = (
            df["GROWTH_SCORE"]
            .mean()
        )

        avg_quality = (
            df["QUALITY_SCORE"]
            .mean()
        )

        avg_ownership = (
            df["OWNERSHIP_SCORE"]
            .mean()
        )

        composite = (

            avg_growth * 0.35 +

            avg_quality * 0.40 +

            avg_ownership * 0.25
        )

        if composite >= 65:

            return "BULLISH"

        elif composite >= 45:

            return "NEUTRAL"

        return "BEARISH"

    except Exception:

        return "UNKNOWN"

# =====================================
# TRADE DECISION ENGINE
# =====================================

def generate_trade_decision(
    final_score
):

    if final_score >= 85:

        return (
            "INSTITUTIONAL STRONG BUY"
        )

    elif final_score >= 72:

        return "BUY"

    elif final_score >= 55:

        return "HOLD"

    elif final_score >= 40:

        return "WEAK"

    return "AVOID"
# =====================================
# FINAL SCORE
# =====================================

def calculate_final_score(row):

    growth = row.get(
        "GROWTH_SCORE",
        0
    )

    quality = row.get(
        "QUALITY_SCORE",
        0
    )

    ownership = row.get(
        "OWNERSHIP_SCORE",
        0
    )

    market_cap = row.get(
        "MARKET_CAP",
        0
    )

    # =====================================
    # WEIGHTED INSTITUTIONAL MODEL
    # =====================================

    final_score = (

        growth * 0.35 +

        quality * 0.40 +

        ownership * 0.25
    )

    # =====================================
    # MARKET CAP BONUS
    # =====================================

    try:

        if market_cap >= 2_000_000_000_000:

            final_score += 8

        elif market_cap >= 500_000_000_000:

            final_score += 5

        elif market_cap >= 100_000_000_000:

            final_score += 2

    except Exception:

        pass

    # =====================================
    # NORMALIZATION
    # =====================================

    final_score = min(
        final_score,
        100
    )

    final_score = max(
        final_score,
        0
    )

    return round(
        final_score,
        2
    )

# =====================================
# INSTITUTIONAL GRADE
# =====================================

def assign_institutional_grade(
    score
):

    if score >= 75:

        return "A"

    elif score >= 60:

        return "B"

    elif score >= 45:

        return "C"

    elif score >= 30:

        return "D"

    return "E"

# =====================================
# MAIN
# =====================================

def main():

    print("=" * 60)

    print(
        "FINAL INSTITUTIONAL "
        "RANKING ENGINE"
    )

    print("=" * 60)

    # ---------------------------------
    # FILE CHECK
    # ---------------------------------

    input_path = Path(
        INPUT_FILE
    )

    if not input_path.exists():

        print(
            f"ERROR: Missing input parquet -> "
            f"{INPUT_FILE}"
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
    # =====================================
    # DATA VALIDATION
    # =====================================

    if "MARKET_CAP" in df.columns:

        df = df[
            df["MARKET_CAP"] > 0
        ]

    df = df.drop_duplicates()

    df = df[
        df["FINAL_SCORE"].notna()
    ]

    # =====================================
    # FINAL SCORE
    # =====================================

    print(
        "\nCalculating final "
        "institutional rankings..."
    )

    df["FINAL_SCORE"] = df.apply(
        calculate_final_score,
        axis=1
    )

    # =====================================
    # MARKET REGIME
    # =====================================

    market_regime = (
        determine_market_regime(df)
    )

    df["MARKET_REGIME"] = (
        market_regime
    )

    # =====================================
    # TRADE DECISION
    # =====================================

    df["TRADE_DECISION"] = (
        df["FINAL_SCORE"]
        .apply(
            generate_trade_decision
        )
    )

    # =====================================
    # RANKING
    # =====================================

    df = df.sort_values(
        by="FINAL_SCORE",
        ascending=False
    )

    df["RANK"] = range(
        1,
        len(df) + 1
    )

    # =====================================
    # INSTITUTIONAL GRADE
    # =====================================

    df["INSTITUTIONAL_GRADE"] = (
        df["FINAL_SCORE"]
        .apply(
            assign_institutional_grade
        )
    )

    # =====================================
    # CREATE OUTPUT DIRS
    # =====================================

    Path(
        "exports"
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

    # =====================================
    # SUMMARY
    # =====================================

    print("\n" + "=" * 60)

    print(
        "INSTITUTIONAL RANKING "
        "COMPLETE"
    )

    print("=" * 60)

    print(
        f"Market Regime: "
        f"{market_regime}"
    )

    print(
        f"\nFinal Dataset Size: "
        f"{len(df)}"
    )

    print(
        "\nTrade Decision Distribution:\n"
    )

    print(
        df["TRADE_DECISION"]
        .value_counts()
    )

    print(
        "\nTop Institutional Stocks:\n"
    )

    print(
        df[
            [
                "RANK",
                "SYMBOL",
                "FINAL_SCORE",
                "TRADE_DECISION",
                "INSTITUTIONAL_GRADE",
                "MARKET_CAP_CATEGORY"
            ]
        ].head(25)
    )

    print(
        f"\nCSV Export:\n"
        f"{CSV_OUTPUT}"
    )

    print(
        f"\nParquet Export:\n"
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
            "\nFATAL RANKING ENGINE ERROR"
        )

        print(str(e))

        traceback.print_exc()

        sys.exit(1)
