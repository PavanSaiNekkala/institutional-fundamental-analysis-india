import pandas as pd
import os


INPUT_FILE = "data/exports/final_rankings.csv"

OUTPUT_FILE = "data/exports/ai_research_reports.csv"


def generate_research_summary(row):

    symbol = row.get("SYMBOL", "UNKNOWN")

    sector = row.get("SECTOR", "UNKNOWN")

    rating = row.get("RATING", "UNAVAILABLE")

    factor_score = round(
        row.get("FACTOR_SCORE", 0),
        2
    )

    final_score = round(
        row.get("FINAL_SCORE", 0),
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

    market_cap = row.get(
        "MARKET_CAP_CATEGORY",
        "UNKNOWN"
    )


    # =====================================
    # AI COMMENTARY
    # =====================================

    summary = f"""
{symbol} operates in the {sector} sector and is currently classified as a {market_cap} company.

The stock currently holds a {rating} institutional rating with a factor score of {factor_score} and a final institutional score of {final_score}.

Business quality metrics remain healthy with Return on Equity (ROE) at {roe}, while revenue growth stands at {revenue_growth}.

Promoter holding is currently {promoter}%, reflecting institutional and management ownership confidence.

The company demonstrates characteristics commonly associated with institutional-quality businesses including scalable operations, sector leadership potential, and factor strength.

Overall institutional outlook for {symbol}: {rating}.
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

    print(
        "Loading institutional rankings dataset..."
    )

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

    print("\n===================================")

    print(
        "AI Institutional Research Reports Generated"
    )

    print("===================================\n")

    print(
        df[
            [
                "SYMBOL",

                "RATING",

                "AI_RESEARCH_SUMMARY"
            ]
        ].head(5)
    )

    print(
        f"\nSaved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":

    main()