import pandas as pd
import yfinance as yf
import os
import time
from datetime import datetime

from utils.sector_classifier import classify_sector
from utils.market_cap_classifier import classify_market_cap


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

        market_cap = info.get("marketCap")

        sector = classify_sector(
            info.get("sector"),
            info.get("industry")
        )

        market_cap_category = classify_market_cap(
            market_cap
        )

        data = {

            "SYMBOL": symbol.replace(".NS", ""),

            "MARKET_CAP": market_cap,

            "MARKET_CAP_CATEGORY": market_cap_category,

            "PE_RATIO": info.get("trailingPE"),

            "PRICE_TO_BOOK": info.get("priceToBook"),

            "ROE": info.get("returnOnEquity"),

            "DEBT_TO_EQUITY": info.get("debtToEquity"),

            "OPERATING_MARGIN": info.get("operatingMargins"),

            "PROFIT_MARGIN": info.get("profitMargins"),

            "REVENUE_GROWTH": info.get("revenueGrowth"),

            "EARNINGS_GROWTH": info.get("earningsGrowth"),

            "CURRENT_PRICE": info.get("currentPrice"),

            "SECTOR": sector,

            "RAW_SECTOR": info.get("sector"),

            "INDUSTRY": info.get("industry"),

            "FETCH_DATE": datetime.now().strftime(
                "%Y-%m-%d"
            )
        }

        return data

    except Exception as e:

        print(
            f"Error fetching {symbol}: {e}"
        )

        return None


def main():

    print("Loading NSE stock universe...")

    stocks = load_stock_universe()

    # Initial stability limit
    stocks = stocks[:200]

    print(
        f"\nTotal Stocks Selected: {len(stocks)}"
    )

    all_data = []

    successful = 0

    failed = 0

    print(
        "\nFetching institutional fundamentals...\n"
    )

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

        # Prevent Yahoo Finance rate limits
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

    print(
        "Institutional Data Collection Complete"
    )

    print("===================================")

    print(f"Successful: {successful}")

    print(f"Failed: {failed}")

    print(
        f"Final Dataset Size: {len(df)}"
    )

    print(f"\nSaved to: {OUTPUT_FILE}")

    print("\nMarket Cap Distribution:\n")

    print(
        df["MARKET_CAP_CATEGORY"]
        .value_counts()
    )

    print("\nSector Distribution:\n")

    print(
        df["SECTOR"]
        .value_counts()
        .head(20)
    )

    print("\nSample Data:\n")

    print(df.head())


if __name__ == "__main__":

    main()
