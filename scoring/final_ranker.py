import pandas as pd
import os


INPUT_FILE = "data/exports/valuation_scores.csv"

OUTPUT_FILE = "data/exports/final_rankings.csv"


def calculate_final_score(df):

    print("Calculating final institutional rankings...")

    df["FINAL_SCORE"] = (

        df["GROWTH_SCORE"] * 0.30 +

        df["QUALITY_SCORE"] * 0.30 +

        df["OWNERSHIP_SCORE"] * 0.20 +

        df["VALUATION_SCORE"] * 0.20
    )

    return df


def assign_rating(score):

    if score >= 75:
        return "STRONG BUY"

    elif score >= 60:
        return "BUY"

    elif score >= 45:
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

        "PE_RATIO",

        "PRICE_TO_BOOK",

        "ROE",

        "REVENUE_GROWTH",

        "EARNINGS_GROWTH",

        "PROMOTER_HOLDING",

        "FII_HOLDING",

        "DII_HOLDING",

        "GROWTH_SCORE",

        "QUALITY_SCORE",

        "OWNERSHIP_SCORE",

        "VALUATION_SCORE",

        "FINAL_SCORE",

        "RATING"
    ]

    available_columns = [
        col for col in columns
        if col in df.columns
    ]

    return df[available_columns]


def main():

    print("Loading valuation-ranked dataset...")

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

    print("\nTop Institutional Picks:\n")

    print(
        final_df.head(20)
    )

    print(
        f"\nFinal rankings saved to: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":

    main()
