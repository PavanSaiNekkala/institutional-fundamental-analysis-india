import pandas as pd
import os


INPUT_FILE = "data/exports/ownership_scores.csv"

OUTPUT_FILE = "data/exports/valuation_scores.csv"


def calculate_valuation_score(df):

    print("Calculating valuation scores...")

    # Lower PE is better
    pe_score = 100 / (
        df["PE_RATIO"].replace(0, 1)
    )

    # Lower PB is better
    pb_score = 100 / (
        df["PRICE_TO_BOOK"].replace(0, 1)
    )

    # PEG Approximation
    growth = (
        df["EARNINGS_GROWTH"]
        .replace(0, 0.01)
        * 100
    )

    peg_ratio = (
        df["PE_RATIO"]
        .replace(0, 1)
        / growth
    )

    peg_score = 100 / (
        peg_ratio.replace(0, 1)
    )

    df["VALUATION_SCORE"] = (

        pe_score * 0.40 +

        pb_score * 0.30 +

        peg_score * 0.30
    )

    return df


def rank_valuation(df):

    df = df.sort_values(
        by="VALUATION_SCORE",
        ascending=False
    )

    df["VALUATION_RANK"] = range(
        1,
        len(df) + 1
    )

    return df


def classify_valuation(score):

    if score >= 70:
        return "UNDERVALUED"

    elif score >= 40:
        return "FAIR VALUE"

    else:
        return "EXPENSIVE"


def main():

    print("Loading ownership dataset...")

    df = pd.read_csv(INPUT_FILE)

    df = calculate_valuation_score(df)

    df = rank_valuation(df)

    df["VALUATION_STATUS"] = df[
        "VALUATION_SCORE"
    ].apply(classify_valuation)

    os.makedirs("data/exports", exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nTop Valuation Opportunities:\n")

    print(
        df[
            [
                "SYMBOL",
                "PE_RATIO",
                "PRICE_TO_BOOK",
                "VALUATION_SCORE",
                "VALUATION_STATUS",
                "VALUATION_RANK"
            ]
        ].head(20)
    )

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()
