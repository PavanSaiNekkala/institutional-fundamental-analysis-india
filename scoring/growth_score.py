import pandas as pd
import os


INPUT_FILE = "data/cleaned/cleaned_fundamentals.csv"
OUTPUT_FILE = "data/exports/growth_scores.csv"


def calculate_growth_score(df):

    print("Calculating institutional growth scores...")

    # Convert growth metrics to percentage scores
    df["REVENUE_GROWTH_SCORE"] = (
        df["REVENUE_GROWTH"].fillna(0) * 100
    )

    df["EARNINGS_GROWTH_SCORE"] = (
        df["EARNINGS_GROWTH"].fillna(0) * 100
    )

    # Final weighted growth score
    df["GROWTH_SCORE"] = (
        df["REVENUE_GROWTH_SCORE"] * 0.5 +
        df["EARNINGS_GROWTH_SCORE"] * 0.5
    )

    return df


def rank_growth_stocks(df):

    df = df.sort_values(
        by="GROWTH_SCORE",
        ascending=False
    )

    df["GROWTH_RANK"] = range(1, len(df) + 1)

    return df


def main():

    print("Loading cleaned institutional dataset...")

    df = pd.read_csv(INPUT_FILE)

    df = calculate_growth_score(df)

    df = rank_growth_stocks(df)

    os.makedirs("data/exports", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nTop Growth Stocks:\n")

    print(
        df[
            [
                "SYMBOL",
                "REVENUE_GROWTH",
                "EARNINGS_GROWTH",
                "GROWTH_SCORE",
                "GROWTH_RANK"
            ]
        ].head(10)
    )

    print(f"\nGrowth rankings saved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()
