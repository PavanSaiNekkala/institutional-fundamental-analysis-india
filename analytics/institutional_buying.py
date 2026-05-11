import pandas as pd
import os


INPUT_FILE = "data/exports/final_rankings.csv"
OUTPUT_FILE = "data/exports/institutional_buying.csv"


def detect_institutional_buying(df):

    print("Detecting institutional accumulation...")

    institutional_df = df[

        (df["OWNERSHIP_SCORE"] > 40) &

        (df["GROWTH_SCORE"] > 15) &

        (df["QUALITY_SCORE"] > 15)

    ]

    institutional_df = institutional_df.sort_values(
        by="FINAL_SCORE",
        ascending=False
    )

    institutional_df["INSTITUTIONAL_RANK"] = range(
        1,
        len(institutional_df) + 1
    )

    return institutional_df


def main():

    print("Loading final institutional rankings...")

    df = pd.read_csv(INPUT_FILE)

    institutional_df = detect_institutional_buying(df)

    os.makedirs("data/exports", exist_ok=True)

    institutional_df.to_csv(OUTPUT_FILE, index=False)

    print("\nInstitutional Accumulation Candidates:\n")

    print(
        institutional_df[
            [
                "INSTITUTIONAL_RANK",
                "SYMBOL",
                "SECTOR",
                "OWNERSHIP_SCORE",
                "GROWTH_SCORE",
                "QUALITY_SCORE",
                "FINAL_SCORE",
                "RATING"
            ]
        ].head(20)
    )

    print(
        f"\nInstitutional buying data saved to: "
        f"{OUTPUT_FILE}"
    )


if __name__ == "__main__":

    main()
