import pandas as pd
import os


INPUT_FILE = "data/exports/final_rankings.csv"
OUTPUT_FILE = "data/exports/sector_rotation.csv"


def analyze_sector_strength(df):

    print("Analyzing sector strength...")

    sector_df = df.groupby("SECTOR").agg({

        "FINAL_SCORE": "mean",

        "GROWTH_SCORE": "mean",

        "QUALITY_SCORE": "mean",

        "OWNERSHIP_SCORE": "mean",

        "SYMBOL": "count"

    }).reset_index()

    sector_df.rename(columns={
        "SYMBOL": "TOTAL_STOCKS"
    }, inplace=True)

    sector_df = sector_df.sort_values(
        by="FINAL_SCORE",
        ascending=False
    )

    sector_df["SECTOR_RANK"] = range(
        1,
        len(sector_df) + 1
    )

    return sector_df


def classify_sector(score):

    if score >= 70:
        return "LEADING"

    elif score >= 55:
        return "STRONG"

    elif score >= 40:
        return "NEUTRAL"

    else:
        return "WEAK"


def main():

    print("Loading institutional rankings...")

    df = pd.read_csv(INPUT_FILE)

    sector_df = analyze_sector_strength(df)

    sector_df["SECTOR_STATUS"] = sector_df[
        "FINAL_SCORE"
    ].apply(classify_sector)

    os.makedirs("data/exports", exist_ok=True)

    sector_df.to_csv(OUTPUT_FILE, index=False)

    print("\nSector Rotation Analysis:\n")

    print(sector_df.head(20))

    print(f"\nSector analysis saved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()
