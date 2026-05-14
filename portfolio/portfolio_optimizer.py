import pandas as pd
import numpy as np

# =========================================================
# NORMALIZE WEIGHTS
# =========================================================

def normalize_weights(weights):

    total = np.sum(weights)

    if total == 0:

        return weights

    return weights / total

# =========================================================
# RISK SCORE
# =========================================================

def calculate_risk_score(df):

    risk = (

        (
            100 - df["QUALITY_SCORE"]
        ) * 0.40

        +

        (
            df["CRASH_RISK_SCORE"]
        ) * 0.40

        +

        (
            100 - df["CONFIDENCE_SCORE"]
        ) * 0.20
    )

    df["PORTFOLIO_RISK_SCORE"] = (

        risk

        .clip(
            lower=0,
            upper=100
        )

        .round(2)
    )

    return df

# =========================================================
# RETURN POTENTIAL
# =========================================================

def expected_return_score(df):

    expected_return = (

        (
            df["GROWTH_SCORE"]
            * 0.35
        )

        +

        (
            df["LEADERSHIP_SCORE"]
            * 0.25
        )

        +

        (
            df[
                "AI_CONVICTION_SCORE"
            ]
            * 0.25
        )

        +

        (
            df[
                "SMART_MONEY_SCORE"
            ]
            * 0.15
        )
    )

    df["EXPECTED_RETURN_SCORE"] = (

        expected_return

        .clip(
            lower=0,
            upper=100
        )

        .round(2)
    )

    return df

# =========================================================
# SHARPE-LIKE SCORE
# =========================================================

def sharpe_like_score(df):

    sharpe = (

        df[
            "EXPECTED_RETURN_SCORE"
        ]

        /

        (
            df[
                "PORTFOLIO_RISK_SCORE"
            ] + 1
        )
    )

    df["SHARPE_LIKE_SCORE"] = (

        sharpe * 20

    ).clip(
        lower=0,
        upper=100
    )

    return df

# =========================================================
# POSITION SIZING
# =========================================================

def calculate_position_size(df):

    weights = (

        (
            df[
                "SHARPE_LIKE_SCORE"
            ]
        )

        *

        (
            df[
                "AI_CONVICTION_SCORE"
            ] / 100
        )
    )

    weights = normalize_weights(
        weights
    )

    df["PORTFOLIO_WEIGHT"] = (

        weights * 100

    ).round(2)

    return df

# =========================================================
# SECTOR DIVERSIFICATION
# =========================================================

def sector_diversification(df):

    max_sector_weight = 25

    diversified = []

    for sector in df["SECTOR"].unique():

        sector_df = df[
            df["SECTOR"] == sector
        ].copy()

        total_weight = (
            sector_df[
                "PORTFOLIO_WEIGHT"
            ].sum()
        )

        if total_weight > max_sector_weight:

            scaling = (

                max_sector_weight
                / total_weight
            )

            sector_df[
                "PORTFOLIO_WEIGHT"
            ] *= scaling

        diversified.append(
            sector_df
        )

    final_df = pd.concat(
        diversified
    )

    final_df[
        "PORTFOLIO_WEIGHT"
    ] = normalize_weights(

        final_df[
            "PORTFOLIO_WEIGHT"
        ]

    ) * 100

    return final_df

# =========================================================
# PORTFOLIO TYPES
# =========================================================

def create_elite_portfolio(df):

    portfolio = df[

        (
            df["ELITE_FLAG"] == 1
        )

        &

        (
            df[
                "AI_CONVICTION_SCORE"
            ] >= 80
        )

    ].copy()

    return portfolio

def create_compounder_portfolio(df):

    portfolio = df[

        (
            df[
                "COMPOUNDER_FLAG"
            ] == 1
        )

        &

        (
            df[
                "CRASH_RISK_SCORE"
            ] <= 40
        )

    ].copy()

    return portfolio

def create_growth_portfolio(df):

    portfolio = df[

        (
            df["GROWTH_SCORE"] >= 80
        )

        &

        (
            df[
                "BREAKOUT_FLAG"
            ] == 1
        )

    ].copy()

    return portfolio

def create_low_risk_portfolio(df):

    portfolio = df[

        (
            df[
                "PORTFOLIO_RISK_SCORE"
            ] <= 35
        )

        &

        (
            df[
                "QUALITY_SCORE"
            ] >= 70
        )

    ].copy()

    return portfolio

# =========================================================
# MASTER OPTIMIZER
# =========================================================

def optimize_portfolio(df):

    df = calculate_risk_score(df)

    df = expected_return_score(df)

    df = sharpe_like_score(df)

    df = calculate_position_size(df)

    df = sector_diversification(df)

    # =====================================================
    # SORT
    # =====================================================

    df = df.sort_values(

        by="PORTFOLIO_WEIGHT",

        ascending=False
    )

    # =====================================================
    # PORTFOLIO OUTPUTS
    # =====================================================

    elite = create_elite_portfolio(df)

    compounders = (
        create_compounder_portfolio(df)
    )

    growth = create_growth_portfolio(df)

    low_risk = (
        create_low_risk_portfolio(df)
    )

    return {

        "MASTER_PORTFOLIO":
            df.head(30),

        "ELITE_PORTFOLIO":
            elite.head(20),

        "COMPOUNDER_PORTFOLIO":
            compounders.head(20),

        "GROWTH_PORTFOLIO":
            growth.head(20),

        "LOW_RISK_PORTFOLIO":
            low_risk.head(20)
    }
