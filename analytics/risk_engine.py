import pandas as pd
import yfinance as yf
import numpy as np
import os


INPUT_FILE = "data/exports/factor_scores.csv"

OUTPUT_FILE = "data/exports/risk_scores.csv"


def calculate_risk_metrics(symbol):

    try:

        ticker = yf.Ticker(f"{symbol}.NS")

        hist = ticker.history(period="1y")

        if hist.empty:

            return None


        # Daily Returns
        hist["RETURNS"] = (
            hist["Close"].pct_change()
        )

        returns = hist["RETURNS"].dropna()


        # Annualized Volatility
        volatility = (
            returns.std() * np.sqrt(252)
        )


        # Sharpe Ratio Approximation
        sharpe = (
            returns.mean() / returns.std()
        ) * np.sqrt(252)


        # Maximum Drawdown
        cumulative = (
            1 + returns
        ).cumprod()

        rolling_max = cumulative.cummax()

        drawdown = (
            cumulative / rolling_max
        ) - 1

        max_drawdown = drawdown.min()


        return {

            "VOLATILITY": volatility,

            "SHARPE_RATIO": sharpe,

            "MAX_DRAWDOWN": max_drawdown
        }

    except Exception as e:

        print(f"Error: {symbol} -> {e}")

        return None


def build_risk_engine(df):

    risk_data = []

    print(
        "\nCalculating institutional risk metrics...\n"
    )

    for index, row in df.iterrows():

        symbol = row["SYMBOL"]

        print(
            f"[{index + 1}/{len(df)}] {symbol}"
        )

        metrics = calculate_risk_metrics(
            symbol
        )

        if metrics:

            risk_data.append({

                "SYMBOL": symbol,

                **metrics
            })


    risk_df = pd.DataFrame(risk_data)

    merged = pd.merge(
        df,
        risk_df,
        on="SYMBOL",
        how="left"
    )

    return merged


def calculate_risk_score(df):

    # Lower volatility preferred
    volatility_score = (
        1 / (
            df["VOLATILITY"]
            .replace(0, np.nan)
        )
    ) * 100


    # Higher sharpe preferred
    sharpe_score = (
        df["SHARPE_RATIO"]
        .fillna(0)
    ) * 10


    # Lower drawdown preferred
    drawdown_score = (
        1 / (
            abs(
                df["MAX_DRAWDOWN"]
            ).replace(0, np.nan)
        )
    ) * 10


    df["RISK_SCORE"] = (

        volatility_score * 0.4 +

        sharpe_score * 0.4 +

        drawdown_score * 0.2
    )

    return df


def rank_risk(df):

    df = df.sort_values(
        by="RISK_SCORE",
        ascending=False
    )

    df["RISK_RANK"] = range(
        1,
        len(df) + 1
    )

    return df


def main():

    print("Loading factor dataset...")

    df = pd.read_csv(INPUT_FILE)

    df = build_risk_engine(df)

    df = calculate_risk_score(df)

    df = rank_risk(df)

    os.makedirs(
        "data/exports",
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nTop Risk-Adjusted Stocks:\n")

    print(
        df[
            [
                "RISK_RANK",

                "SYMBOL",

                "VOLATILITY",

                "SHARPE_RATIO",

                "MAX_DRAWDOWN",

                "RISK_SCORE"
            ]
        ].head(20)
    )

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()
