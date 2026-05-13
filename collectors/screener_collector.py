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

from utils.market_cap_classifier import classify_market_cap


# =====================================
# CONFIGURATION
# =====================================

INPUT_FILE = "data/raw/yfinance_stock_urls.xlsx"

CSV_OUTPUT = (
    "data/financials/fundamentals.csv"
)

PARQUET_OUTPUT = (
    "data/cache/parquet/"
    "fundamentals.parquet"
)

# -------------------------------------
# GITHUB SAFE SETTINGS
# -------------------------------------

MAX_STOCKS = 300

MAX_WORKERS = 3

REQUEST_DELAY = 1


# =====================================
# LOAD STOCK UNIVERSE
# =====================================

def load_stock_universe():

    try:

        if not os.path.exists(INPUT_FILE):

            print(
                f"ERROR: File not found -> "
                f"{INPUT_FILE}"
            )

            sys.exit(1)

        print(
            "\nLoading Excel universe..."
        )

        df = pd.read_excel(INPUT_FILE)

        if df.empty:

            print(
                "ERROR: Input Excel is empty"
            )

            sys.exit(1)

        # ---------------------------------
        # SYMBOL COLUMN
        # ---------------------------------

        if "SYMBOL" in df.columns:

            symbols = (
                df["SYMBOL"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

        # ---------------------------------
        # YFINANCE URL COLUMN
        # ---------------------------------

        elif "YFINANCE_URL" in df.columns:

            symbols = []

            for url in (
                df["YFINANCE_URL"]
                .dropna()
                .astype(str)
            ):

                try:

                    symbol = (
                        url.split("/quote/")[1]
                        .split("?")[0]
                    )

                    symbols.append(symbol)

                except Exception:

                    continue

        else:

            print(
                "ERROR: Missing SYMBOL "
                "or YFINANCE_URL column"
            )

            sys.exit(1)

        # ---------------------------------
        # CLEAN SYMBOLS
        # ---------------------------------

        cleaned_symbols = []

        for symbol in symbols:

            symbol = symbol.strip()

            if not symbol.endswith(".NS"):

                symbol = f"{symbol}.NS"

            cleaned_symbols.append(symbol)

        cleaned_symbols = sorted(
            list(set(cleaned_symbols))
        )

        print(
            f"Loaded "
            f"{len(cleaned_symbols)} "
            f"stocks"
        )

        return cleaned_symbols

    except Exception as e:

        print(
            f"ERROR loading stock universe: "
            f"{e}"
        )

        traceback.print_exc()

        sys.exit(1)


# =====================================
# FETCH FUNDAMENTALS
# =====================================

def fetch_fundamentals(symbol):

    retries = 3

    for attempt in range(retries):

        try:

            time.sleep(REQUEST_DELAY)

            stock = yf.Ticker(symbol)

            fast_info = stock.fast_info

            market_cap = (
                fast_info.get(
                    "market_cap",
                    0
                )
            )

            current_price = (
                fast_info.get(
                    "lastPrice",
                    0
                )
            )

            data = {

                "SYMBOL":
                    symbol.replace(
                        ".NS",
                        ""
                    ),

                "MARKET_CAP":
                    market_cap,

                "MARKET_CAP_CATEGORY":
                    classify_market_cap(
                        market_cap
                    ),

                "CURRENT_PRICE":
                    current_price,

                # Placeholder fields
                "PE_RATIO": 0,

                "PRICE_TO_BOOK": 0,

                "ROE": 0,

                "DEBT_TO_EQUITY": 0,

                "OPERATING_MARGIN": 0,

                "PROFIT_MARGIN": 0,

                "REVENUE_GROWTH": 0,

                "EARNINGS_GROWTH": 0,

                "SECTOR": "Unknown",

                "RAW_SECTOR": "Unknown",

                "INDUSTRY": "Unknown",

                "FETCH_DATE":
                    datetime.now()
                    .strftime(
                        "%Y-%m-%d"
                    )
            }

            return data

        except Exception as e:

            error_msg = str(e)

            print(
                f"Retry {attempt + 1}/3 "
                f"for {symbol}: "
                f"{error_msg}"
            )

            # -----------------------------
            # RATE LIMIT HANDLING
            # -----------------------------

            if (
                "Too Many Requests"
                in error_msg
            ):

                time.sleep(10)

            else:

                time.sleep(3)

    print(f"FAILED: {symbol}")

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

    stocks = load_stock_universe()

    # ---------------------------------
    # LIMIT FOR GITHUB STABILITY
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
                    f"{stock_symbol}: "
                    f"{e}"
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
    # CREATE OUTPUT DIRECTORIES
    # =====================================

    os.makedirs(
        "data/financials",
        exist_ok=True
    )

    os.makedirs(
        "data/cache/parquet",
        exist_ok=True
    )

    # =====================================
    # SAVE CSV + PARQUET
    # =====================================

    try:

        # CSV export
        df.to_csv(
            CSV_OUTPUT,
            index=False
        )

        # PARQUET export
        df.to_parquet(
            PARQUET_OUTPUT,
            index=False
        )

        print(
            "\nSaved CSV + "
            "Parquet cache"
        )

    except Exception as e:

        print(
            f"ERROR saving outputs: "
            f"{e}"
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
        f"\nCSV Saved To:\n"
        f"{CSV_OUTPUT}"
    )

    print(
        f"\nParquet Saved To:\n"
        f"{PARQUET_OUTPUT}"
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
