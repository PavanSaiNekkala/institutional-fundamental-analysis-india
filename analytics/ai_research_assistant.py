import pandas as pd
import os


INPUT_FILE = "data/exports/risk_scores.csv"

OUTPUT_FILE = "data/exports/ai_research_reports.csv"


def generate_research_summary(row):

    symbol = row["SYMBOL"]

    sector = row["SECTOR"]

    rating = row["RATING"]

    factor_score = round(
        row["FACTOR_SCORE"],
        2
    )

    final_score = round(
        row["FINAL_SCORE"],
        2
    )

    roe = round(
        row.get("ROE", 0),
        2
    )

    revenue_growth = round(
        row.get("REVENUE_GROWTH", 0),
        2
    )

    promoter = round(
        row.get("PROMOTER_HOLDING", 0),
        2
    )


    # =====================================
    # AI COMMENTARY
    # =====================================

    summary = f"""
{symbol} operates in the {sector} sector and currently holds a {rating} institutional rating.

The company has a factor score of {factor_score} and a final institutional score of {final_score}.

Business quality remains strong with ROE at {roe}, while revenue growth stands at {revenue_growth}.

Promoter holding is currently {promoter}%, indicating ownership confidence.

The stock demonstrates characteristics associated with institutional-quality businesses including scalable operations, factor strength, and sector positioning.

Overall institutional outlook: {rating}.
"""

    return summary.strip()


def generate_ai_reports(df):

    print(
        "Generating AI institutional research reports..."
    )

    df["AI_RESEARCH_SUMMARY"] = df.apply(
        generate_research_summary,
        axis=1
    )

    return df


def main():

    print("Loading institutional risk dataset...")

    df = pd.read_csv(INPUT_FILE)

    df = generate_ai_reports(df)

    os.makedirs(
        "data/exports",
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nAI Research Reports Generated\n")

    print(
        df[
            [
                "SYMBOL",

                "RATING",

                "AI_RESEARCH_SUMMARY"
            ]
        ].head(5)
    )

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()
