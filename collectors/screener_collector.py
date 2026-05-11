import pandas as pd
import yfinance as yf
import os
from datetime import datetime


STOCKS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "HAL.NS",
    "BEL.NS",
    "NTPC.NS",
    "POWERGRID.NS"
]


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
            "FETCH_DATE": datetime.now().strftime("%Y-%m-%d")
        }

        return data

    except Exception as e:

        print(f"Error fetching {symbol}: {e}")

        return None


def main():

    all_data = []

    print("Fetching institutional fundamentals...\n")

    for stock in STOCKS:

        print(f"Fetching: {stock}")

        data = fetch_fundamentals(stock)

        if data:
            all_data.append(data)

    df = pd.DataFrame(all_data)

    os.makedirs("data/financials", exist_ok=True)

    output_path = "data/financials/fundamentals.csv"

    df.to_csv(output_path, index=False)

    print("\nFundamentals collected successfully.")

    print(df.head())

    print(f"\nSaved to: {output_path}")


if __name__ == "__main__":
    main()
