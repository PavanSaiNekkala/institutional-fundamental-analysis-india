import pandas as pd
import numpy as np

# =========================================================
# MARKET BREADTH
# =========================================================

def calculate_market_breadth(df):

    advancing = len(

        df[
            df["FINAL_SCORE"] >= 70
        ]

    )

    declining = len(

        df[
            df["FINAL_SCORE"] < 40
        ]

    )

    total = len(df)

    if total == 0:

        return 0

    breadth = (

        (
            advancing - declining
        ) / total

    ) * 100

    return round(
        breadth,
        2
    )

# =========================================================
# SECTOR MOMENTUM
# =========================================================

def sector_momentum(df):

    sector_scores = (

        df

        .groupby("SECTOR")[
            "FINAL_SCORE"
        ]

        .mean()

        .sort_values(
            ascending=False
        )
    )

    return sector_scores

# =========================================================
# VOLATILITY REGIME
# =========================================================

def volatility_regime(df):

    std_dev = (
        df["FINAL_SCORE"]
        .std()
    )

    if std_dev >= 25:

        return "HIGH VOLATILITY"

    elif std_dev >= 15:

        return "MODERATE VOLATILITY"

    return "LOW VOLATILITY"

# =========================================================
# SMART MONEY FLOW
# =========================================================

def smart_money_flow(df):

    institutional = len(

        df[
            (
                df[
                    "TRADE_DECISION"
                ]

                ==

                "INSTITUTIONAL STRONG BUY"
            )
        ]

    )

    elite = len(

        df[
            df["ELITE_FLAG"] == 1
        ]

    )

    compounders = len(

        df[
            df["COMPOUNDER_FLAG"] == 1
        ]

    )

    score = (

        (
            institutional * 0.5
        )

        +

        (
            elite * 0.3
        )

        +

        (
            compounders * 0.2
        )
    )

    return round(
        score,
        2
    )

# =========================================================
# RISK REGIME
# =========================================================

def risk_regime(df):

    aggressive = len(

        df[
            df["SECTOR"].isin(
                [
                    "Technology",
                    "Automobiles",
                    "Emerging",
                    "Industrials"
                ]
            )
        ]

    )

    defensive = len(

        df[
            df["SECTOR"].isin(
                [
                    "Healthcare",
                    "Consumer",
                    "Utilities"
                ]
            )
        ]

    )

    if aggressive > defensive * 1.5:

        return "RISK ON"

    elif defensive > aggressive:

        return "RISK OFF"

    return "BALANCED"

# =========================================================
# MASTER ENGINE
# =========================================================

def generate_market_regime(df):

    breadth = calculate_market_breadth(df)

    volatility = volatility_regime(df)

    risk = risk_regime(df)

    smart_money = smart_money_flow(df)

    sector_strength = sector_momentum(df)

    top_sector = (
        sector_strength.index[0]
        if len(sector_strength) > 0
        else "UNKNOWN"
    )

    # =====================================================
    # FINAL REGIME
    # =====================================================

    if breadth >= 40 and risk == "RISK ON":

        regime = "STRONG BULL MARKET"

    elif breadth >= 15:

        regime = "BULL MARKET"

    elif breadth >= -10:

        regime = "SIDEWAYS MARKET"

    elif breadth >= -30:

        regime = "WEAK MARKET"

    else:

        regime = "BEAR MARKET"

    return {

        "MARKET_REGIME":
            regime,

        "MARKET_BREADTH":
            breadth,

        "VOLATILITY_REGIME":
            volatility,

        "RISK_REGIME":
            risk,

        "SMART_MONEY_SCORE":
            smart_money,

        "LEADING_SECTOR":
            top_sector
    }
