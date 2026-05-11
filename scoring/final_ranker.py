import pandas as pd
import os


INPUT_FILE = "data/exports/ownership_scores.csv"
OUTPUT_FILE = "data/exports/final_rankings.csv"


def calculate_final_score(df):

    print("Calculating final institutional rankings...")

    df["FINAL_SCORE"] = (

        df["GROWTH_SCORE"] * 0.40 +

        df["QUALITY_SCORE"] * 0.35 +

        df["OWNERSHIP_SCORE"] * 0.25
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

    df["FINAL_RANK"] = range(1, len(df) + 1)

    df["RATING"] = df["FINAL_SCORE"].apply(assign_rating)

    return df


def main():

    print("Loading institutional scoring dataset...")

    df = pd.read_csv(INPUT_FILE)

    df = calculate_final_score(df)

    df = rank_stocks(df)

    os.makedirs("data/exports", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nTop Institutional Picks:\n")

    print(
        df[
            [
                "FINAL_RANK",
                "SYMBOL",
                "SECTOR",
                "GROWTH_SCORE",
                "QUALITY_SCORE",
                "OWNERSHIP_SCORE",
                "FINAL_SCORE",
                "RATING"
            ]
        ].head(20)
    )

    print(f"\nFinal rankings saved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()
