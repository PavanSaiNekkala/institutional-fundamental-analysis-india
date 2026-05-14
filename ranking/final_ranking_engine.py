# =========================================================
# PROJECT ROOT FIX
# =========================================================

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# =========================================================
# IMPORTS
# =========================================================

import pandas as pd
import numpy as np
import traceback
import warnings

from analytics.market_regime_engine import (
    generate_market_regime
)

from ai.institutional_ai_engine import (
    run_ai_engine
)

from portfolio.portfolio_optimizer import (
    optimize_portfolio
)

from alerts.smart_alert_engine import (
    generate_alerts
)

warnings.filterwarnings("ignore")

# =========================================================
# DIRECTORIES
# =========================================================

BASE_DIR = ROOT

DATA_DIR = (
    BASE_DIR
    / "data"
    / "cache"
    / "parquet"
)

EXPORT_DIR = (
    BASE_DIR
    / "exports"
)

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)

EXPORT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

# =========================================================
# FILE PATHS
# =========================================================

INPUT_FILE = (
    DATA_DIR
    / "ownership_scored.parquet"
)

CSV_OUTPUT = (
    EXPORT_DIR
    / "institutional_rankings.csv"
)

PARQUET_OUTPUT = (
    DATA_DIR
    / "institutional_rankings.parquet"
)

# =========================================================
# REQUIRED COLUMNS
# =========================================================

REQUIRED_COLUMNS = [

    "SYMBOL",
    "SECTOR",
    "SUBSECTOR",

    "GROWTH_SCORE",
    "QUALITY_SCORE",
    "OWNERSHIP_SCORE",

    "HIGH_QUALITY_FLAG",
    "HIGH_GROWTH_FLAG",
    "COMPOUNDER_FLAG"
]

# =========================================================
# PERCENTILE ENGINE
# =========================================================

def percentile_rank(series):

    return (

        series.rank(
            pct=True
        ) * 100

    ).round(2)

# =========================================================
# VALIDATION
# =========================================================

def validate_columns(df):

    missing = [

        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:

        raise ValueError(
            f"Missing required columns: {missing}"
        )

# =========================================================
# SECTOR RELATIVE SCORES
# =========================================================

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

                df.groupby(
                    "SECTOR"
                )[col]

                .transform(
                    percentile_rank
                )
            )

    return df

# =========================================================
# SUBSECTOR RELATIVE SCORES
# =========================================================

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

# =========================================================
# INSTITUTIONAL BREADTH
# =========================================================

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

# =========================================================
# LEADERSHIP SCORE
# =========================================================

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

# =========================================================
# CONFIDENCE SCORE
# =========================================================

def confidence_score(df):

    df["CONFIDENCE_SCORE"] = (

        (
            df["LEADERSHIP_SCORE"]
            * 0.40
        )

        +

        (
            df["INSTITUTIONAL_BREADTH"]
            * 0.30
        )

        +

        (
            df["GROWTH_SCORE_SECTOR_REL"]
            * 0.15
        )

        +

        (
            df["QUALITY_SCORE_SECTOR_REL"]
            * 0.15
        )

    ).round(2)

    return df

# =========================================================
# FINAL SCORE
# =========================================================

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

    if "MARKET_CAP" in df.columns:

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

# =========================================================
# ELITE FILTER
# =========================================================

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

# =========================================================
# TRADE DECISION
# =========================================================

def generate_trade_decision(score):

    if score >= 90:
        return "INSTITUTIONAL ELITE"

    elif score >= 82:
        return "INSTITUTIONAL STRONG BUY"

    elif score >= 70:
        return "BUY"

    elif score >= 55:
        return "HOLD"

    elif score >= 40:
        return "WEAK"

    return "AVOID"

# =========================================================
# INSTITUTIONAL GRADE
# =========================================================

def assign_institutional_grade(score):

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

# =========================================================
# MAIN
# =========================================================

def main():

    print("=" * 70)
    print("AI INSTITUTIONAL RANKING ENGINE")
    print("=" * 70)

    if not INPUT_FILE.exists():

        print(
            f"\nERROR: Missing parquet file:\n{INPUT_FILE}"
        )

        sys.exit(1)

    try:

        print("\nLoading parquet dataset...")

        df = pd.read_parquet(
            INPUT_FILE
        )

    except Exception as e:

        print(f"\nERROR loading parquet:\n{e}")

        traceback.print_exc()

        sys.exit(1)

    if df.empty:

        print("\nERROR: Empty dataset")

        sys.exit(1)

    print(f"\nLoaded dataset size: {len(df)}")

    # =====================================================
    # VALIDATION
    # =====================================================

    validate_columns(df)

    # =====================================================
    # CLEANING
    # =====================================================

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    df = df.fillna(0)

    df = df.drop_duplicates()

    if "MARKET_CAP" in df.columns:

        df = df[
            df["MARKET_CAP"] > 0
        ]

    # =====================================================
    # CORE ENGINE
    # =====================================================

    print("\nRunning institutional engines...")

    df = sector_relative_scores(df)

    df = subsector_relative_scores(df)

    df = institutional_breadth(df)

    df = market_leadership_score(df)

    df = confidence_score(df)

    df = calculate_final_score(df)

    df = elite_filter(df)

    # =====================================================
    # MARKET REGIME
    # =====================================================

    market_data = (
        generate_market_regime(df)
    )

    for key, value in market_data.items():

        df[key] = value

    # =====================================================
    # TRADE DECISION
    # =====================================================

    df["TRADE_DECISION"] = (

        df["FINAL_SCORE"]

        .apply(
            generate_trade_decision
        )
    )

    # =====================================================
    # AI ENGINE
    # =====================================================

    print("\nRunning AI engine...")

    df, insights = (
        run_ai_engine(df)
    )

    # =====================================================
    # RANKING
    # =====================================================

    df = df.sort_values(

        by="FINAL_SCORE",

        ascending=False
    )

    df["RANK"] = range(

        1,

        len(df) + 1
    )

    # =====================================================
    # GRADES
    # =====================================================

    df["INSTITUTIONAL_GRADE"] = (

        df["FINAL_SCORE"]

        .apply(
            assign_institutional_grade
        )
    )

    # =====================================================
    # PORTFOLIOS
    # =====================================================

    print("\nOptimizing portfolios...")

    portfolios = (
        optimize_portfolio(df)
    )

    # =====================================================
    # ALERTS
    # =====================================================

    print("\nGenerating smart alerts...")

    alerts_df = (
        generate_alerts(df)
    )

    # =====================================================
    # SAVE OUTPUTS
    # =====================================================

    print("\nSaving outputs...")

    df.to_csv(
        CSV_OUTPUT,
        index=False
    )

    df.to_parquet(
        PARQUET_OUTPUT,
        index=False
    )

    # =====================================================
    # SAVE PORTFOLIOS
    # =====================================================

    for name, portfolio_df in portfolios.items():

        output_path = (
            EXPORT_DIR
            / f"{name.lower()}.csv"
        )

        portfolio_df.to_csv(
            output_path,
            index=False
        )

        print(f"Saved: {output_path}")

    # =====================================================
    # SAVE ALERTS
    # =====================================================

    alerts_output = (
        EXPORT_DIR
        / "smart_alerts.csv"
    )

    alerts_df.to_csv(
        alerts_output,
        index=False
    )

    print(f"Saved: {alerts_output}")

    # =====================================================
    # SUMMARY
    # =====================================================

    print("\n" + "=" * 70)
    print("AI INSTITUTIONAL PIPELINE COMPLETE")
    print("=" * 70)

    print(
        f"\nMarket Regime: "
        f"{market_data['MARKET_REGIME']}"
    )

    print(
        f"\nRisk Regime: "
        f"{market_data['RISK_REGIME']}"
    )

    print(
        f"\nVolatility Regime: "
        f"{market_data['VOLATILITY_REGIME']}"
    )

    print(
        f"\nLeading Sector: "
        f"{market_data['LEADING_SECTOR']}"
    )

    print(
        f"\nDataset Size: "
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
                "AI_CONVICTION_SCORE",
                "CONFIDENCE_SCORE",
                "TRADE_DECISION",
                "INSTITUTIONAL_GRADE",
                "ELITE_FLAG"
            ]
        ]

        .head(25)

    )

    print(
        f"\nCSV Export:\n{CSV_OUTPUT}"
    )

    print(
        f"\nParquet Export:\n{PARQUET_OUTPUT}"
    )

# =========================================================
# ENTRY
# =========================================================

if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print("\nFATAL PIPELINE ERROR")

        print(str(e))

        traceback.print_exc()

        sys.exit(1)
