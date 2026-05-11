import pandas as pd
import numpy as np
import os


INPUT_FILE = "data/exports/valuation_scores.csv"

OUTPUT_FILE = "data/exports/factor_scores.csv"


def percentile_score(series, ascending=True):

    return series.rank(
        pct=True,
        ascending=ascending
    ) * 100


def build_factor_model(df):

    print("Building institutional factor model...")


    # =====================================
    # QUALITY FACTOR
    # =====================================

    df["ROE_FACTOR"] = percentile_score(
        df["ROE"].fillna(0),
        ascending=True
    )

    df["MARGIN_FACTOR"] = percentile_score(
        df["OPERATING_MARGIN"].fillna(0),
        ascending=True
    )

    df["DEBT_FACTOR"] = percentile_score(
        df["DEBT_TO_EQUITY"].fillna(0),
        ascending=False
    )


    df["QUALITY_FACTOR"] = (

        df["ROE_FACTOR"] * 0.4 +

        df["MARGIN_FACTOR"] * 0.4 +

        df["DEBT_FACTOR"] * 0.2
    )


    # =====================================
    # GROWTH FACTOR
    # =====================================

    df["REVENUE_FACTOR"] = percentile_score(
        df["REVENUE_GROWTH"].fillna(0),
        ascending=True
    )

    df["EARNINGS_FACTOR"] = percentile_score(
        df["EARNINGS_GROWTH"].fillna(0),
        ascending=True
    )


    df["GROWTH_FACTOR"] = (

        df["REVENUE_FACTOR"] * 0.5 +

        df["EARNINGS_FACTOR"] * 0.5
    )


    # =====================================
    # VALUE FACTOR
    # =====================================

    df["PE_FACTOR"] = percentile_score(
        df["PE_RATIO"].replace(0, np.nan),
        ascending=False
    )

    df["PB_FACTOR"] = percentile_score(
        df["PRICE_TO_BOOK"].replace(0, np.nan),
        ascending=False
    )


    df["VALUE_FACTOR"] = (

        df["PE_FACTOR"] * 0.5 +

        df["PB_FACTOR"] * 0.5
    )


    # =====================================
    # OWNERSHIP FACTOR
    # =====================================

    df["PROMOTER_FACTOR"] = percentile_score(
        df["PROMOTER_HOLDING"].fillna(0),
        ascending=True
    )

    df["FII_FACTOR"] = percentile_score(
        df["FII_HOLDING"].fillna(0),
        ascending=True
    )


    df["OWNERSHIP_FACTOR"] = (

        df["PROMOTER_FACTOR"] * 0.5 +

        df["FII_FACTOR"] * 0.5
    )


    # =====================================
    # FINAL FACTOR SCORE
    # =====================================

    df["FACTOR_SCORE"] = (

        df["QUALITY_FACTOR"] * 0.30 +

        df["GROWTH_FACTOR"] * 0.30 +

        df["VALUE_FACTOR"] * 0.20 +

        df["OWNERSHIP_FACTOR"] * 0.20
    )


    return df


def rank_factor_stocks(df):

    df = df.sort_values(
        by="FACTOR_SCORE",
        ascending=False
    )

    df["FACTOR_RANK"] = range(
        1,
        len(df) + 1
    )

    return df


def classify_factor_quality(score):

    if score >= 80:

        return "ELITE"

    elif score >= 65:

        return "STRONG"

    elif score >= 50:

        return "AVERAGE"

    else:

        return "WEAK"


def main():

    print("Loading valuation dataset...")

    df = pd.read_csv(INPUT_FILE)

    df = build_factor_model(df)

    df = rank_factor_stocks(df)

    df["FACTOR_GRADE"] = df[
        "FACTOR_SCORE"
    ].apply(classify_factor_quality)

    os.makedirs(
        "data/exports",
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nTop Institutional Factor Stocks:\n")

    print(
        df[
            [
                "FACTOR_RANK",

                "SYMBOL",

                "SECTOR",

                "MARKET_CAP_CATEGORY",

                "FACTOR_SCORE",

                "FACTOR_GRADE"
            ]
        ].head(20)
    )

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()
