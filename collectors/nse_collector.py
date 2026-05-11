import pandas as pd
from nsepython import nse_eq_symbols
import os
from datetime import datetime


OUTPUT_FILE = "data/raw/nse_stock_universe.csv"


def fetch_nse_universe():

    print("Fetching NSE stock universe...")

    symbols = nse_eq_symbols()

    cleaned_symbols = []

    for symbol in symbols:

        cleaned_symbols.append(
            f"{symbol}.NS"
        )

    df = pd.DataFrame({

        "SYMBOL": cleaned_symbols,

        "FETCH_DATE": datetime.now().strftime(
            "%Y-%m-%d"
        )
    })

    return df


def save_universe(df):

    os.makedirs(
        "data/raw",
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nSaved to: {OUTPUT_FILE}")


def main():

    df = fetch_nse_universe()

    print(df.head())

    print(f"\nTotal Stocks: {len(df)}")

    save_universe(df)


if __name__ == "__main__":

    main()
