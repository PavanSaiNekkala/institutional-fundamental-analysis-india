import pandas as pd
import os


INPUT_FILE = "data/exports/factor_scores.csv"

OUTPUT_FILE = "data/exports/model_portfolio.csv"


TOP_N = 20


def build_model_portfolio(df):

    print("Building institutional model portfolio...")


    # Select top factor stocks
    portfolio = df.sort_values(
        by="FACTOR_SCORE",
        ascending=False
    ).head(TOP_N)


    # Equal weight allocation
    portfolio["PORTFOLIO_WEIGHT"] = (
        100 / TOP_N
    )


    # Portfolio rank
    portfolio["PORTFOLIO_RANK"] = range(
        1,
        len(portfolio) + 1
    )

    return portfolio


def portfolio_summary(portfolio):

    print("\n===================================")

    print("INSTITUTIONAL MODEL PORTFOLIO")

    print("===================================\n")


    # Average factor score
    avg_factor = round(
        portfolio["FACTOR_SCORE"].mean(),
        2
    )

    print(
        f"Average Factor Score: {avg_factor}"
    )


    # Sector allocation
    print("\nSector Allocation:\n")

    sector_alloc = portfolio[
        "SECTOR"
    ].value_counts(normalize=True) * 100

    print(
        sector_alloc.round(2)
    )


    # Market cap allocation
    print("\nMarket Cap Allocation:\n")

    market_cap_alloc = portfolio[
        "MARKET_CAP_CATEGORY"
    ].value_counts(normalize=True) * 100

    print(
        market_cap_alloc.round(2)
    )


def main():

    print("Loading factor model dataset...")

    df = pd.read_csv(INPUT_FILE)

    portfolio = build_model_portfolio(df)

    portfolio_summary(portfolio)

    os.makedirs(
        "data/exports",
        exist_ok=True
    )

    portfolio.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()
