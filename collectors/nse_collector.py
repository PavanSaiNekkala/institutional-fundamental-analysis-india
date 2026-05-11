import pandas as pd
from nsepython import nse_eq_symbols
from datetime import datetime
import os


def fetch_nse_stock_universe():
    """
    Fetch all NSE equity symbols
    """

    print("Fetching NSE stock universe...")

    symbols = nse_eq_symbols()

    df = pd.DataFrame({
        "SYMBOL": symbols
    })

    df["FETCH_DATE"] = datetime.now().strftime("%Y-%m-%d")

    return df


def save_stock_universe(df):
    """
    Save NSE stock universe
    """

    os.makedirs("data/raw", exist_ok=True)

    output_path = "data/raw/nse_stock_universe.csv"

    df.to_csv(output_path, index=False)

    print(f"Saved stock universe to: {output_path}")


def main():

    df = fetch_nse_stock_universe()

    print(df.head())

    print(f"\nTotal Stocks: {len(df)}")

    save_stock_universe(df)


if __name__ == "__main__":
    main()
