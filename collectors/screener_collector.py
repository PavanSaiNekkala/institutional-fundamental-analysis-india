import os
import sys
import time
import traceback
import warnings
from datetime import datetime
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed
)

import pandas as pd
import numpy as np
import yfinance as yf

warnings.filterwarnings("ignore")

# =====================================================
# PROJECT ROOT FIX
# =====================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

if PROJECT_ROOT not in sys.path:

    sys.path.insert(
        0,
        PROJECT_ROOT
    )

from utils.market_cap_classifier import (
    classify_market_cap
)

# =====================================================
# CONFIGURATION
# =====================================================

INPUT_FILE = (
    "data/raw/"
    "yfinance_stock_urls.xlsx"
)

CSV_OUTPUT = (
    "data/financials/"
    "fundamentals.csv"
)

PARQUET_OUTPUT = (
    "data/cache/parquet/"
    "fundamentals.parquet"
)

FAILED_OUTPUT = (
    "exports/"
    "failed_symbols.csv"
)

MAX_STOCKS = 3000
MAX_WORKERS = 8
REQUEST_DELAY = 0.15

# =====================================================
# LOAD STOCK UNIVERSE
# =====================================================

def load_stock_universe():

    try:

        if not os.path.exists(INPUT_FILE):

            print(
                f"ERROR: Missing file -> "
                f"{INPUT_FILE}"
            )

            sys.exit(1)

        print(
            "\nLoading stock universe..."
        )

        df = pd.read_excel(INPUT_FILE)

        if df.empty:

            print(
                "ERROR: Empty input file"
            )

            sys.exit(1)

        if "SYMBOL" in df.columns:

            symbols = (
                df["SYMBOL"]
                .dropna()
                .astype(str)
                .tolist()
            )

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
                "ERROR: Missing "
                "SYMBOL/YFINANCE_URL"
            )

            sys.exit(1)

        cleaned_symbols = []

        for symbol in symbols:

            symbol = (
                str(symbol)
                .strip()
                .upper()
            )

            if not symbol.endswith(".NS"):

                symbol = f"{symbol}.NS"

            cleaned_symbols.append(symbol)

        cleaned_symbols = sorted(
            list(set(cleaned_symbols))
        )

        print(
            f"Loaded "
            f"{len(cleaned_symbols)} "
            f"symbols"
        )

        return cleaned_symbols

    except Exception as e:

        print(
            f"Universe loading error: "
            f"{e}"
        )

        traceback.print_exc()

        sys.exit(1)

# =====================================================
# SAFE NUMERIC
# =====================================================

def safe_numeric(value):

    try:

        if str(value).strip().lower() in [

            "infinity",
            "-infinity",
            "inf",
            "-inf",
            "nan",
            "none",
            "",
        ]:

            return np.nan

        value = float(value)

        if np.isinf(value):

            return np.nan

        return value

    except Exception:

        return np.nan

# =====================================================
# FETCH FUNDAMENTALS
# =====================================================

def fetch_fundamentals(symbol):

    retries = 3

    for attempt in range(retries):

        try:

            time.sleep(REQUEST_DELAY)

            stock = yf.Ticker(symbol)

            fast_info = stock.fast_info

            info = stock.info

            market_cap = (
                fast_info.get(
                    "market_cap",
                    None
                )
            )

            if not market_cap:

                market_cap = (
                    info.get(
                        "marketCap",
                        0
                    )
                )

            current_price = (
                fast_info.get(
                    "lastPrice",
                    None
                )
            )

            if not current_price:

                current_price = (
                    info.get(
                        "currentPrice",
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
                    safe_numeric(
                        market_cap
                    ),

                "MARKET_CAP_CATEGORY":
                    classify_market_cap(
                        market_cap
                    ),

                "CURRENT_PRICE":
                    safe_numeric(
                        current_price
                    ),

                # =====================================
                # HARD FIX FOR PE_RATIO
                # =====================================

                "PE_RATIO":
                    (
                        np.nan

                        if str(
                            info.get(
                                "trailingPE",
                                np.nan
                            )
                        ).strip().lower()

                        in [
                            "infinity",
                            "-infinity",
                            "inf",
                            "-inf",
                            "nan",
                            "none",
                            "",
                        ]

                        else pd.to_numeric(
                            info.get(
                                "trailingPE",
                                np.nan
                            ),
                            errors="coerce"
                        )
                    ),

                "PRICE_TO_BOOK":
                    safe_numeric(
                        info.get(
                            "priceToBook",
                            np.nan
                        )
                    ),

                "ROE":
                    safe_numeric(
                        info.get(
                            "returnOnEquity",
                            np.nan
                        )
                    ),

                "DEBT_TO_EQUITY":
                    safe_numeric(
                        info.get(
                            "debtToEquity",
                            np.nan
                        )
                    ),

                "OPERATING_MARGIN":
                    safe_numeric(
                        info.get(
                            "operatingMargins",
                            np.nan
                        )
                    ),

                "PROFIT_MARGIN":
                    safe_numeric(
                        info.get(
                            "profitMargins",
                            np.nan
                        )
                    ),

                "REVENUE_GROWTH":
                    safe_numeric(
                        info.get(
                            "revenueGrowth",
                            np.nan
                        )
                    ),

                "EARNINGS_GROWTH":
                    safe_numeric(
                        info.get(
                            "earningsGrowth",
                            np.nan
                        )
                    ),

                "SECTOR":
                    str(
                        info.get(
                            "sector",
                            "Unknown"
                        )
                    ),

                "RAW_SECTOR":
                    str(
                        info.get(
                            "sector",
                            "Unknown"
                        )
                    ),

                "INDUSTRY":
                    str(
                        info.get(
                            "industry",
                            "Unknown"
                        )
                    ),

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
                f"Retry "
                f"{attempt + 1}/3 "
                f"for {symbol}: "
                f"{error_msg}"
            )

            if (
                "Too Many Requests"
                in error_msg
            ):

                time.sleep(8)

            else:

                time.sleep(2)

    print(f"FAILED: {symbol}")

    return None

# =====================================================
# MAIN
# =====================================================

def main():

    print("=" * 60)

    print(
        "INSTITUTIONAL FUNDAMENTAL "
        "COLLECTOR"
    )

    print("=" * 60)

    stocks = load_stock_universe()

    stocks = stocks[:MAX_STOCKS]

    print(
        f"\nStocks Selected: "
        f"{len(stocks)}"
    )

    all_data = []
    failed_symbols = []

    successful = 0
    failed = 0

    start_time = time.time()

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
                    f"{stock_symbol}"
                )

                if data:

                    all_data.append(data)

                    successful += 1

                else:

                    failed += 1

                    failed_symbols.append(
                        stock_symbol
                    )

            except Exception as e:

                print(
                    f"ERROR: "
                    f"{stock_symbol} -> "
                    f"{e}"
                )

                failed += 1

                failed_symbols.append(
                    stock_symbol
                )

    df = pd.DataFrame(all_data)

    if df.empty:

        print(
            "\nERROR: No data collected"
        )

        sys.exit(1)

    print(
        "\nApplying dataframe cleaning..."
    )

    INVALID_VALUES = [

        "Infinity",
        "-Infinity",
        "inf",
        "-inf",
        "INF",
        "-INF",
        "NaN",
        "nan",
        "None",
        "none",
        "NULL",
        "null",
        "",
    ]

    df = df.replace(
        INVALID_VALUES,
        np.nan
    )

    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    NUMERIC_COLUMNS = [

        "MARKET_CAP",
        "CURRENT_PRICE",
        "PE_RATIO",
        "PRICE_TO_BOOK",
        "ROE",
        "DEBT_TO_EQUITY",
        "OPERATING_MARGIN",
        "PROFIT_MARGIN",
        "REVENUE_GROWTH",
        "EARNINGS_GROWTH",
    ]

    for col in NUMERIC_COLUMNS:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

            df[col] = (
                df[col]
                .replace(
                    [np.inf, -np.inf],
                    np.nan
                )
                .astype("float64")
            )

    for col in df.columns:

        if df[col].dtype == "object":

            df[col] = (
                df[col]
                .fillna("")
                .astype(str)
            )

    df = df.drop_duplicates()

    if "MARKET_CAP" in df.columns:

        df = df[
            df["MARKET_CAP"].fillna(0) > 0
        ]

    if "CURRENT_PRICE" in df.columns:

        df = df[
            df["CURRENT_PRICE"].fillna(0) > 0
        ]

    os.makedirs(
        "data/financials",
        exist_ok=True
    )

    os.makedirs(
        "data/cache/parquet",
        exist_ok=True
    )

    os.makedirs(
        "exports",
        exist_ok=True
    )

    try:

        print(
            "\nSaving CSV..."
        )

        df.to_csv(
            CSV_OUTPUT,
            index=False
        )

        # ==========================================
        # FINAL HARD TYPE ENFORCEMENT
        # ==========================================

        for col in df.columns:

            try:

                converted = pd.to_numeric(
                    df[col],
                    errors="ignore"
                )

                df[col] = converted

            except Exception:

                pass

        if "PE_RATIO" in df.columns:

            df["PE_RATIO"] = pd.to_numeric(
                df["PE_RATIO"],
                errors="coerce"
            )

            df["PE_RATIO"] = (
                df["PE_RATIO"]
                .replace(
                    [np.inf, -np.inf],
                    np.nan
                )
                .astype("float64")
            )

        for col in df.select_dtypes(
            include=["object"]
        ).columns:

            df[col] = (
                df[col]
                .astype(str)
                .replace(
                    [
                        "Infinity",
                        "-Infinity",
                        "inf",
                        "-inf",
                        "nan",
                        "None",
                    ],
                    ""
                )
            )

        print("\nFINAL DTYPES:\n")

        print(df.dtypes)

        print(
            "\nSaving parquet dataset..."
        )

        df.to_parquet(
            PARQUET_OUTPUT,
            index=False,
            engine="pyarrow"
        )

        print(
            "\nSaved CSV + "
            "Parquet outputs"
        )

    except Exception as e:

        print(
            f"Save error: {e}"
        )

        traceback.print_exc()

        sys.exit(1)

    if failed_symbols:

        failed_df = pd.DataFrame({

            "FAILED_SYMBOLS":
                failed_symbols

        })

        failed_df.to_csv(
            FAILED_OUTPUT,
            index=False
        )

    end_time = time.time()

    runtime = round(
        (end_time - start_time) / 60,
        2
    )

    print("\n" + "=" * 60)

    print(
        "DATA COLLECTION COMPLETE"
    )

    print("=" * 60)

    print(
        f"Successful: "
        f"{successful}"
    )

    print(
        f"Failed: "
        f"{failed}"
    )

    print(
        f"Final Dataset Size: "
        f"{len(df)}"
    )

    print(
        f"Runtime: "
        f"{runtime} minutes"
    )

    print(
        f"\nCSV:\n"
        f"{CSV_OUTPUT}"
    )

    print(
        f"\nParquet:\n"
        f"{PARQUET_OUTPUT}"
    )

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
