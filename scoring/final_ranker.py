import pandas as pd
import os


INPUT_FILE = "data/exports/factor_scores.csv"

OUTPUT_FILE = "data/exports/final_rankings.csv"


def calculate_final_score(df):

    print("Calculating final institutional rankings...")

    if "RISK_SCORE" not in df.columns:

        df["RISK_SCORE"] = 0


    df["FINAL_SCORE"] = (

        df["QUALITY_FACTOR"] * 0.25 +

        df["GROWTH_FACTOR"] * 0.25 +

        df["VALUE_FACTOR"] * 0.15 +

        df["OWNERSHIP_FACTOR"] * 0.15 +

        df["FACTOR_SCORE"] * 0.10 +

        df["RISK_SCORE"] * 0.10
    )

    return df


def assign_rating(score):

    if score >= 80:

        return "STRONG BUY"

    elif score >= 65:

        return "BUY"

    elif score >= 50:

        return "WATCH"

    else:

        return "AVOID"


def rank_stocks(df):

    df = df.sort_values(
        by="FINAL_SCORE",
        ascending=False
    )

    df["FINAL_RANK"] = range(
        1,
        len(df) + 1
    )

    df["RATING"] = df[
        "FINAL_SCORE"
    ].apply(assign_rating)

    return df


def select_output_columns(df):

    columns = [

        "FINAL_RANK",

        "SYMBOL",

        "SECTOR",

        "MARKET_CAP",

        "MARKET_CAP_CATEGORY",

        "PE_RATIO",

        "PRICE_TO_BOOK",

        "ROE",

        "DEBT_TO_EQUITY",

        "OPERATING_MARGIN",

        "PROFIT_MARGIN",

        "REVENUE_GROWTH",

        "EARNINGS_GROWTH",

        "PROMOTER_HOLDING",

        "FII_HOLDING",

        "DII_HOLDING",

        "PLEDGE_PERCENT",

        "GROWTH_SCORE",

        "QUALITY_SCORE",

        "OWNERSHIP_SCORE",

        "VALUATION_SCORE",

        "QUALITY_FACTOR",

        "GROWTH_FACTOR",

        "VALUE_FACTOR",

        "OWNERSHIP_FACTOR",

        "FACTOR_SCORE",

        "RISK_SCORE",

        "FINAL_SCORE",

        "RATING"
    ]

    available_columns = [
        col for col in columns
        if col in df.columns
    ]

    return df[available_columns]


def main():

    print("Loading institutional factor dataset...")

    df = pd.read_csv(INPUT_FILE)

    df = calculate_final_score(df)

    df = rank_stocks(df)

    final_df = select_output_columns(df)

    os.makedirs(
        "data/exports",
        exist_ok=True
    )

    final_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n===================================")

    print(
        "Final Institutional Rankings Generated"
    )

    print("===================================\n")

    print(
        final_df.head(20)
    )

    print(
        f"\nSaved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":

    main()