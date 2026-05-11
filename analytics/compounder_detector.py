import pandas as pd
import os


INPUT_FILE = "data/exports/final_rankings.csv"
OUTPUT_FILE = "data/exports/compounders.csv"


def detect_compounders(df):

    print("Detecting institutional compounders...")

    compounders = df[

        (df["ROE"] > 0.15) &

        (df["REVENUE_GROWTH"] > 0.10) &

        (df["EARNINGS_GROWTH"] > 0.10) &

        (df["DEBT_TO_EQUITY"] < 1)

    ]

    compounders = compounders.sort_values(
        by="FINAL_SCORE",
        ascending=False
    )

    compounders["COMPOUNDER_RANK"] = range(
        1,
        len(compounders) + 1
    )

    return compounders


def main():

    print("Loading institutional rankings...")

    df = pd.read_csv(INPUT_FILE)

    compounders = detect_compounders(df)

    os.makedirs("data/exports", exist_ok=True)

    compounders.to_csv(OUTPUT_FILE, index=False)

    print("\nTop Institutional Compounders:\n")

    print(
        compounders[
            [
                "COMPOUNDER_RANK",
                "SYMBOL",
                "SECTOR",
                "ROE",
                "REVENUE_GROWTH",
                "EARNINGS_GROWTH",
                "FINAL_SCORE",
                "RATING"
            ]
        ].head(20)
    )

    print(f"\nCompounder list saved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()
