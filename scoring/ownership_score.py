import pandas as pd
import os


INPUT_FILE = "data/exports/quality_scores.csv"

OWNERSHIP_FILE = "data/ownership/shareholding.csv"

OUTPUT_FILE = "data/exports/ownership_scores.csv"


def load_ownership_data():

    ownership_df = pd.read_csv(
        OWNERSHIP_FILE
    )

    return ownership_df


def merge_ownership(df, ownership_df):

    merged_df = pd.merge(
        df,
        ownership_df,
        on="SYMBOL",
        how="left"
    )

    return merged_df


def calculate_ownership_score(df):

    print("Calculating real ownership scores...")

    promoter_score = (
        df["PROMOTER_HOLDING"].fillna(0) * 0.35
    )

    fii_score = (
        df["FII_HOLDING"].fillna(0) * 0.30
    )

    dii_score = (
        df["DII_HOLDING"].fillna(0) * 0.25
    )

    pledge_penalty = (
        df["PLEDGE_PERCENT"].fillna(0) * 0.10
    )

    df["OWNERSHIP_SCORE"] = (

        promoter_score +

        fii_score +

        dii_score -

        pledge_penalty
    )

    return df


def rank_ownership(df):

    df = df.sort_values(
        by="OWNERSHIP_SCORE",
        ascending=False
    )

    df["OWNERSHIP_RANK"] = range(
        1,
        len(df) + 1
    )

    return df


def main():

    print("Loading quality scores...")

    df = pd.read_csv(INPUT_FILE)

    ownership_df = load_ownership_data()

    df = merge_ownership(df, ownership_df)

    df = calculate_ownership_score(df)

    df = rank_ownership(df)

    os.makedirs("data/exports", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nTop Ownership Ranked Stocks:\n")

    print(
        df[
            [
                "SYMBOL",
                "PROMOTER_HOLDING",
                "FII_HOLDING",
                "DII_HOLDING",
                "OWNERSHIP_SCORE",
                "OWNERSHIP_RANK"
            ]
        ].head(10)
    )

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()
