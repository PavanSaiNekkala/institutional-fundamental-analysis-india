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
# PERCENTILE ENGINE
# =====================================

def percentile_rank(series):

    return (

        series.rank(
            pct=True
        ) * 100

    ).round(2)

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

        if composite >= 70:

            return "STRONG BULLISH"

        elif composite >= 55:

            return "BULLISH"

        elif composite >= 45:

            return "NEUTRAL"

        elif composite >= 35:

            return "WEAK"

        return "BEARISH"

    except Exception:

        return "UNKNOWN"

# =====================================
# SECTOR RELATIVE SCORES
# =====================================

def sector_relative_scores(df):

    score_columns = [

        "GROWTH_SCORE",
        "QUALITY_SCORE",
        "OWNERSHIP_SCORE"

    ]

    for col in score_columns:

        if col in df.columns:

            df[
                f"{col}_SECTOR_REL"
            ] = (

                df.groupby("SECTOR")[col]

                .transform(
                    percentile_rank
                )
            )

    return df

# =====================================
# SUBSECTOR RELATIVE SCORES
# =====================================

def subsector_relative_scores(df):

    score_columns = [

        "GROWTH_SCORE",
        "QUALITY_SCORE",
        "OWNERSHIP_SCORE"

    ]

    for col in score_columns:

        if col in df.columns:

            df[
                f"{col}_SUBSECTOR_REL"
            ] = (

                df.groupby(
                    "SUBSECTOR"
                )[col]

                .transform(
                    percentile_rank
                )
            )

    return df

# =====================================
# INSTITUTIONAL BREADTH
# =====================================

def institutional_breadth(df):

    df["INSTITUTIONAL_BREADTH"] = (

        (
            df["HIGH_QUALITY_FLAG"]

            +

            df["HIGH_GROWTH_FLAG"]

            +

            df["COMPOUNDER_FLAG"]
        ) / 3

    ) * 100

    return df

# =====================================
# LEADERSHIP SCORE
# =====================================

def market_leadership_score(df):

    leadership = (

        (
            df["GROWTH_SCORE"]
            * 0.40
        )

        +

        (
            df["QUALITY_SCORE"]
            * 0.35
        )

        +

        (
            df["OWNERSHIP_SCORE"]
            * 0.25
        )

    )

    df["LEADERSHIP_SCORE"] = (

        percentile_rank(
            leadership
        )

    )

    return df

# =====================================
# CONFIDENCE SCORE
# =====================================

def confidence_score(df):

    df["CONFIDENCE_SCORE"] = (

        (
            df["LEADERSHIP_SCORE"]
            * 0.40
        )

        +

        (
            df[
                "INSTITUTIONAL_BREADTH"
            ]
            * 0.30
        )

        +

        (
            df[
                "GROWTH_SCORE_SECTOR_REL"
            ]
            * 0.15
        )

        +

        (
            df[
                "QUALITY_SCORE_SECTOR_REL"
            ]
            * 0.15
        )

    ).round(2)

    return df

# =====================================
# FINAL SCORE
# =====================================

def calculate_final_score(df):

    df["FINAL_SCORE"] = (

        (
            df["CONFIDENCE_SCORE"]
            * 0.40
        )

        +

        (
            df["LEADERSHIP_SCORE"]
            * 0.25
        )

        +

        (
            df["GROWTH_SCORE"]
            * 0.20
        )

        +

        (
            df["QUALITY_SCORE"]
            * 0.15
        )

    )

    # =====================================
    # MARKET CAP BONUS
    # =====================================

    df["FINAL_SCORE"] += np.where(

        df["MARKET_CAP"] >= 2_000_000_000_000,

        8,

        np.where(

            df["MARKET_CAP"] >= 500_000_000_000,

            5,

            np.where(

                df["MARKET_CAP"] >= 100_000_000_000,

                2,

                0
            )
        )
    )

    df["FINAL_SCORE"] = (

        df["FINAL_SCORE"]

        .clip(
            lower=0,
            upper=100
        )

        .round(2)
    )

    return df

# =====================================
# ELITE FILTER
# =====================================

def elite_filter(df):

    df["ELITE_FLAG"] = np.where(

        (
            (df["FINAL_SCORE"] >= 85)
            &
            (df["CONFIDENCE_SCORE"] >= 80)
            &
            (df["COMPOUNDER_FLAG"] == 1)
        ),

        1,

        0
    )

    return df

# =====================================
# TRADE DECISION ENGINE
# =====================================

def generate_trade_decision(
    final_score
):

    if final_score >= 90:

        return (
            "INSTITUTIONAL ELITE"
        )

    elif final_score >= 82:

        return (
            "INSTITUTIONAL STRONG BUY"
        )

    elif final_score >= 70:

        return "BUY"

    elif final_score >= 55:

        return "HOLD"

    elif final_score >= 40:

        return "WEAK"

    return "AVOID"

# =====================================
# INSTITUTIONAL GRADE
# =====================================

def assign_institutional_grade(
    score
):

    if score >= 85:

        return "A+"

    elif score >= 75:

        return "A"

    elif score >= 65:

        return "B"

    elif score >= 50:

        return "C"

    elif score >= 35:

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

    input_path = Path(
        INPUT_FILE
    )

    if not input_path.exists():

        print(
            f"ERROR: Missing parquet -> "
            f"{INPUT_FILE}"
        )

        sys.exit(1)

    # =====================================
    # LOAD DATA
    # =====================================

    try:

        print(
            "\nLoading parquet..."
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

    # =====================================
    # CLEAN DATA
    # =====================================

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    df = df.fillna(0)

    df = df.drop_duplicates()

    # =====================================
    # VALIDATION
    # =====================================

    if "MARKET_CAP" in df.columns:

        df = df[
            df["MARKET_CAP"] > 0
        ]

    # =====================================
    # INSTITUTIONAL ENGINES
    # =====================================

    print(
        "\nCalculating institutional rankings..."
    )

    df = sector_relative_scores(df)

    df = subsector_relative_scores(df)

    df = institutional_breadth(df)

    df = market_leadership_score(df)

    df = confidence_score(df)

    df = calculate_final_score(df)

    df = elite_filter(df)

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
    # OUTPUT DIRECTORIES
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
        "INSTITUTIONAL RANKING COMPLETE"
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
                "SECTOR",
                "SUBSECTOR",
                "FINAL_SCORE",
                "CONFIDENCE_SCORE",
                "TRADE_DECISION",
                "INSTITUTIONAL_GRADE",
                "ELITE_FLAG"
            ]
        ]

        .head(25)

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
