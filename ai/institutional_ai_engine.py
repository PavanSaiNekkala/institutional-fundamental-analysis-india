import pandas as pd
import numpy as np

# =========================================================
# ANOMALY DETECTION
# =========================================================

def detect_anomalies(df):

    conditions = (

        (
            df["GROWTH_SCORE"] >= 90
        )

        &

        (
            df["QUALITY_SCORE"] < 40
        )

    )

    df["ANOMALY_FLAG"] = np.where(

        conditions,

        1,

        0
    )

    return df

# =========================================================
# COMPOUNDER PROBABILITY
# =========================================================

def compounder_probability(df):

    probability = (

        (
            df["QUALITY_SCORE"]
            * 0.40
        )

        +

        (
            df["GROWTH_SCORE"]
            * 0.35
        )

        +

        (
            df["OWNERSHIP_SCORE"]
            * 0.15
        )

        +

        (
            df["CONFIDENCE_SCORE"]
            * 0.10
        )

    )

    df["COMPOUNDER_PROBABILITY"] = (

        probability

        .clip(
            lower=0,
            upper=100
        )

        .round(2)
    )

    return df

# =========================================================
# CRASH RISK ENGINE
# =========================================================

def crash_risk(df):

    risk = (

        (
            100 - df["QUALITY_SCORE"]
        ) * 0.45

        +

        (
            100 - df["CONFIDENCE_SCORE"]
        ) * 0.35

        +

        (
            100 - df["OWNERSHIP_SCORE"]
        ) * 0.20
    )

    df["CRASH_RISK_SCORE"] = (

        risk

        .clip(
            lower=0,
            upper=100
        )

        .round(2)
    )

    return df

# =========================================================
# SMART MONEY ACCUMULATION
# =========================================================

def smart_money_accumulation(df):

    accumulation = (

        (
            df["OWNERSHIP_SCORE"]
            * 0.50
        )

        +

        (
            df["CONFIDENCE_SCORE"]
            * 0.25
        )

        +

        (
            df["LEADERSHIP_SCORE"]
            * 0.25
        )
    )

    df["SMART_MONEY_SCORE"] = (

        accumulation

        .clip(
            lower=0,
            upper=100
        )

        .round(2)
    )

    return df

# =========================================================
# BREAKOUT DETECTION
# =========================================================

def detect_breakouts(df):

    breakout = (

        (
            df["GROWTH_SCORE"] >= 80
        )

        &

        (
            df["LEADERSHIP_SCORE"] >= 75
        )

        &

        (
            df["SMART_MONEY_SCORE"] >= 70
        )
    )

    df["BREAKOUT_FLAG"] = np.where(

        breakout,

        1,

        0
    )

    return df

# =========================================================
# AI CONVICTION SCORE
# =========================================================

def ai_conviction_score(df):

    conviction = (

        (
            df["FINAL_SCORE"]
            * 0.30
        )

        +

        (
            df["CONFIDENCE_SCORE"]
            * 0.25
        )

        +

        (
            df["SMART_MONEY_SCORE"]
            * 0.25
        )

        +

        (
            df[
                "COMPOUNDER_PROBABILITY"
            ]
            * 0.20
        )
    )

    df["AI_CONVICTION_SCORE"] = (

        conviction

        .clip(
            lower=0,
            upper=100
        )

        .round(2)
    )

    return df

# =========================================================
# AI WATCHLIST
# =========================================================

def generate_ai_watchlist(df):

    watchlist = (

        (
            df["AI_CONVICTION_SCORE"] >= 80
        )

        &

        (
            df["CRASH_RISK_SCORE"] <= 35
        )

        &

        (
            df["BREAKOUT_FLAG"] == 1
        )
    )

    df["AI_WATCHLIST"] = np.where(

        watchlist,

        1,

        0
    )

    return df

# =========================================================
# AI MARKET INSIGHTS
# =========================================================

def generate_market_insights(df):

    insights = []

    # =====================================================
    # TOP SECTOR
    # =====================================================

    top_sector = (

        df

        .groupby("SECTOR")[
            "FINAL_SCORE"
        ]

        .mean()

        .idxmax()
    )

    insights.append(
        f"Leading sector: {top_sector}"
    )

    # =====================================================
    # BREAKOUT COUNT
    # =====================================================

    breakout_count = int(

        df[
            "BREAKOUT_FLAG"
        ].sum()
    )

    insights.append(
        f"Breakout candidates: "
        f"{breakout_count}"
    )

    # =====================================================
    # ELITE STOCKS
    # =====================================================

    elite_count = int(

        df[
            "ELITE_FLAG"
        ].sum()
    )

    insights.append(
        f"Elite institutional stocks: "
        f"{elite_count}"
    )

    # =====================================================
    # RISK ANALYSIS
    # =====================================================

    avg_risk = round(

        df[
            "CRASH_RISK_SCORE"
        ].mean(),

        2
    )

    insights.append(
        f"Average crash risk: "
        f"{avg_risk}"
    )

    return insights

# =========================================================
# MASTER AI ENGINE
# =========================================================

def run_ai_engine(df):

    df = detect_anomalies(df)

    df = compounder_probability(df)

    df = crash_risk(df)

    df = smart_money_accumulation(df)

    df = detect_breakouts(df)

    df = ai_conviction_score(df)

    df = generate_ai_watchlist(df)

    insights = generate_market_insights(df)

    return df, insights
