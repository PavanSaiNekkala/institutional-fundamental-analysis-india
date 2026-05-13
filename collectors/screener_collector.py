import os
import sys
import time
import traceback
import warnings
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import numpy as np
import yfinance as yf

warnings.filterwarnings("ignore")

# =====================================
# PROJECT ROOT PATH FIX
# =====================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.sector_classifier import classify_sector
from utils.market_cap_classifier import classify_market_cap


# =====================================
# CONFIGURATION
# =====================================

UNIVERSE_FILE = "data/raw/nse_stock_universe.csv"

OUTPUT_FILE = "data/financials/fundamentals.csv"

MAX_STOCKS = 500

MAX_WORKERS = 10


# =====================================
# LOAD STOCK UNIVERSE
# =====================================

def load_stock_universe():

    try:

        if not os.path.exists(UNIVERSE_FILE):

            print(
                f"ERROR: Universe file missing -> "
                f"{UNIVERSE_FILE}"
            )

            sys.exit(1)

        df = pd.read_csv(
            UNIVERSE_FILE
        )

        if df.empty:

            print(
                "ERROR: Universe file is empty"
            )

            sys.exit(1)

        if "SYMBOL" not in df.columns:

            print(
                "ERROR: SYMBOL column missing"
            )

            sys.exit(1)

        stocks = (
            df["SYMBOL"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        return stocks

    except Exception as e:

        print(
            f"ERROR loading universe: {e}"
        )

        traceback.print_exc()

        sys.exit(1)


# =====================================
# FETCH FUNDAMENTALS
# =====================================

def fetch_fundamentals(symbol):

    try:

        if not symbol.endswith(".NS"):

            symbol = f"{symbol}.NS"

        stock = yf.Ticker(symbol)

        try:
            info = stock.fast_info
        except Exception:
            info = {}

        try:
            full_info = stock.info
        except Exception:
            full_info = {}

        market_cap = (
            info.get("market_cap")
            or full_info.get("marketCap")
            or 0
        )

        sector = classify_sector(
            full_info.get("sector"),
            full_info.get("industry")
        )

        market_cap_category = classify_market_cap(
            market_cap
        )

        data = {

            "SYMBOL": symbol.replace(".NS", ""),

            "MARKET_CAP": market_cap,

            "MARKET_CAP_CATEGORY":
                market_cap_category,

            "PE_RATIO":
                full_info.get("trailingPE", 0),

            "PRICE_TO_BOOK":
                full_info.get("priceToBook", 0),

            "ROE":
                full_info.get("returnOnEquity", 0),

            "DEBT_TO_EQUITY":
                full_info.get("debtToEquity", 0),

            "OPERATING_MARGIN":
                full_info.get("operatingMargins", 0),

            "PROFIT_MARGIN":
                full_info.get("profitMargins", 0),

            "REVENUE_GROWTH":
                full_info.get("revenueGrowth", 0),

            "EARNINGS_GROWTH":
                full_info.get("earningsGrowth", 0),

            "CURRENT_PRICE":
                info.get("lastPrice")
                or full_info.get("currentPrice", 0),

            "SECTOR": sector,

            "RAW_SECTOR":
                full_info.get("sector", "Unknown"),

            "INDUSTRY":
                full_info.get("industry", "Unknown"),

            "FETCH_DATE":
                datetime.now().strftime(
                    "%Y-%m-%d"
                )
        }

        return data

    except Exception as e:

        print(
            f"FAILED: {symbol} -> {e}"
        )

        return None


# =====================================
# MAIN EXECUTION
# =====================================

def main():

    print("=" * 60)

    print(
        "INSTITUTIONAL FUNDAMENTAL "
        "COLLECTOR"
    )

    print("=" * 60)

    print(
        "\nLoading NSE stock universe..."
    )

    stocks = load_stock_universe()

    # ---------------------------------
    # LIMIT FOR STABILITY
    # ---------------------------------

    stocks = stocks[:MAX_STOCKS]

    print(
        f"\nTotal Stocks Selected: "
        f"{len(stocks)}"
    )

    print(
        f"Parallel Workers: "
        f"{MAX_WORKERS}"
    )

    print(
        "\nFetching institutional "
        "fundamentals...\n"
    )

    all_data = []

    successful = 0

    failed = 0

    start_time = time.time()

    # =====================================
    # PARALLEL EXECUTION
    # =====================================

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        future_to_stock = {

            executor.submit(
                fetch_fundamentals,
                stock
            ): stock

            for stock in stocks
        }

        completed = 0

        for future in as_completed(
            future_to_stock
        ):

            stock_symbol = (
                future_to_stock[future]
            )

            completed += 1

            try:

                data = future.result()

                print(
                    f"[{completed}/"
                    f"{len(stocks)}] "
                    f"Completed: "
                    f"{stock_symbol}"
                )

                if data:

                    all_data.append(data)

                    successful += 1

                else:

                    failed += 1

            except Exception as e:

                print(
                    f"ERROR processing "
                    f"{stock_symbol}: {e}"
                )

                failed += 1

    # =====================================
    # CREATE DATAFRAME
    # =====================================

    df = pd.DataFrame(all_data)

    if df.empty:

        print(
            "\nERROR: No valid stock "
            "data collected"
        )

        sys.exit(1)

    # =====================================
    # CLEAN DATA
    # =====================================

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    df = df.fillna(0)

    df = df.drop_duplicates()

    # =====================================
    # CREATE OUTPUT DIRECTORY
    # =====================================

    os.makedirs(
        "data/financials",
        exist_ok=True
    )

    # =====================================
    # SAVE CSV
    # =====================================

    try:

        df.to_csv(
            OUTPUT_FILE,
            index=False
        )

    except Exception as e:

        print(
            f"ERROR saving CSV: {e}"
        )

        traceback.print_exc()

        sys.exit(1)

    # =====================================
    # FINAL SUMMARY
    # =====================================

    end_time = time.time()

    runtime = round(
        (end_time - start_time) / 60,
        2
    )

    print("\n" + "=" * 60)

    print(
        "INSTITUTIONAL DATA "
        "COLLECTION COMPLETE"
    )

    print("=" * 60)

    print(
        f"Successful: {successful}"
    )

    print(
        f"Failed: {failed}"
    )

    print(
        f"Final Dataset Size: "
        f"{len(df)}"
    )

    print(
        f"Runtime: {runtime} minutes"
    )

    print(
        f"\nSaved to: "
        f"{OUTPUT_FILE}"
    )

    # =====================================
    # ANALYTICS
    # =====================================

    try:

        if (
            "MARKET_CAP_CATEGORY"
            in df.columns
        ):

            print(
                "\nMarket Cap "
                "Distribution:\n"
            )

            print(
                df[
                    "MARKET_CAP_CATEGORY"
                ].value_counts()
            )

        if "SECTOR" in df.columns:

            print(
                "\nSector Distribution:\n"
            )

            print(
                df["SECTOR"]
                .value_counts()
                .head(20)
            )

        print("\nSample Data:\n")

        print(df.head())

    except Exception as e:

        print(
            f"Analytics display "
            f"error: {e}"
        )


# =====================================
# ENTRY POINT
# =====================================

if __name__ == "__main__":

    try:

        main()

    except Exception as e:

        print(
            "\nFATAL PIPELINE ERROR"
        )

        print(str(e))

        traceback.print_exc()

        sys.exit(1)
