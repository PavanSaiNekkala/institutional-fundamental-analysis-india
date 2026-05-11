import pandas as pd
import os


INPUT_FILE = "data/exports/growth_scores.csv"
OUTPUT_FILE = "data/exports/quality_scores.csv"


def calculate_quality_score(df):

    print("Calculating institutional quality scores...")

    # ROE Score
    df["ROE_SCORE"] = (
        df["ROE"].fillna(0) * 100
    )

    # Operating Margin Score
    df["OPERATING_MARGIN_SCORE"] = (
        df["OPERATING_MARGIN"].fillna(0) * 100
    )

    # Profit Margin Score
    df["PROFIT_MARGIN_SCORE"] = (
        df["PROFIT_MARGIN"].fillna(0) * 100
    )

    # Debt Penalty
    df["DEBT_PENALTY"] = (
        df["DEBT_TO_EQUITY"].fillna(0)
    )

    # Final Quality Score
    df["QUALITY_SCORE"] = (
        df["ROE_SCORE"] * 0.35 +
        df["OPERATING_MARGIN_SCORE"] * 0.30 +
        df["PROFIT_MARGIN_SCORE"] * 0.25 -
        df["DEBT_PENALTY"] * 0.10
    )

    return df


def rank_quality_stocks(df):

    df = df.sort_values(
        by="QUALITY_SCORE",
        ascending=False
    )

    df["QUALITY_RANK"] = range(1, len(df) + 1)

    return df


def main():

    print("Loading institutional growth dataset...")

    df = pd.read_csv(INPUT_FILE)

    df = calculate_quality_score(df)

    df = rank_quality_stocks(df)

    os.makedirs("data/exports", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nTop Quality Stocks:\n")

    print(
        df[
            [
                "SYMBOL",
                "ROE",
                "OPERATING_MARGIN",
                "PROFIT_MARGIN",
                "DEBT_TO_EQUITY",
                "QUALITY_SCORE",
                "QUALITY_RANK"
            ]
        ].head(10)
    )

    print(f"\nQuality rankings saved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()
