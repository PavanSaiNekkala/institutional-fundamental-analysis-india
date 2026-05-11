import pandas as pd
import yfinance as yf
import os
import time
from datetime import datetime


UNIVERSE_FILE = "data/raw/nse_stock_universe.csv"

OUTPUT_FILE = "data/financials/fundamentals.csv"


def load_stock_universe():

    df = pd.read_csv(
        UNIVERSE_FILE
    )

    stocks = df["SYMBOL"].tolist()

    return stocks


def fetch_fundamentals(symbol):

    try:

        stock = yf.Ticker(symbol)

        info = stock.info

        data = {

            "SYMBOL": symbol.replace(".NS", ""),

            "MARKET_CAP": info.get("marketCap"),

            "PE_RATIO": info.get("trailingPE"),

            "PRICE_TO_BOOK": info.get("priceToBook"),

            "ROE": info.get("returnOnEquity"),

            "DEBT_TO_EQUITY": info.get("debtToEquity"),

            "OPERATING_MARGIN": info.get("operatingMargins"),

            "PROFIT_MARGIN": info.get("profitMargins"),

            "REVENUE_GROWTH": info.get("revenueGrowth"),

            "EARNINGS_GROWTH": info.get("earningsGrowth"),

            "CURRENT_PRICE": info.get("currentPrice"),

            "SECTOR": info.get("sector"),

            "INDUSTRY": info.get("industry"),

            "FETCH_DATE": datetime.now().strftime(
                "%Y-%m-%d"
            )
        }

        return data

    except Exception as e:

        print(f"Error fetching {symbol}: {e}")

        return None


def main():

    print("Loading NSE stock universe...")

    stocks = load_stock_universe()

    # Initial stability limit
    stocks = stocks[:200]

    print(f"\nTotal Stocks Selected: {len(stocks)}")

    all_data = []

    successful = 0

    failed = 0

    print("\nFetching institutional fundamentals...\n")

    for index, stock_symbol in enumerate(stocks):

        print(
            f"[{index + 1}/{len(stocks)}] "
            f"Fetching: {stock_symbol}"
        )

        data = fetch_fundamentals(
            stock_symbol
        )

        if data:

            all_data.append(data)

            successful += 1

        else:

            failed += 1

        # Prevent rate limiting
        time.sleep(0.5)

    df = pd.DataFrame(all_data)

    os.makedirs(
        "data/financials",
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\n===================================")

    print("Institutional Data Collection Complete")

    print("===================================")

    print(f"Successful: {successful}")

    print(f"Failed: {failed}")

    print(f"Final Dataset Size: {len(df)}")

    print(f"\nSaved to: {OUTPUT_FILE}")

    print("\nSample Data:\n")

    print(df.head())


if __name__ == "__main__":

    main()
