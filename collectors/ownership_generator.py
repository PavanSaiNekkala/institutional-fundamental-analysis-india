import pandas as pd
import numpy as np
import os


INPUT_FILE = "data/financials/fundamentals.csv"

OUTPUT_FILE = "data/ownership/shareholding.csv"


def estimate_promoter_holding(sector):

    sector = str(sector).upper()

    if sector in [

        "IT",

        "BANKING",

        "NBFC"
    ]:

        return np.random.uniform(10, 35)

    elif sector in [

        "DEFENCE",

        "POWER",

        "PSU"
    ]:

        return np.random.uniform(50, 75)

    else:

        return np.random.uniform(35, 65)


def estimate_fii_holding(market_cap_category):

    category = str(
        market_cap_category
    ).upper()

    if category == "LARGE CAP":

        return np.random.uniform(20, 45)

    elif category == "MID CAP":

        return np.random.uniform(10, 25)

    else:

        return np.random.uniform(2, 15)


def estimate_dii_holding(market_cap_category):

    category = str(
        market_cap_category
    ).upper()

    if category == "LARGE CAP":

        return np.random.uniform(10, 30)

    elif category == "MID CAP":

        return np.random.uniform(5, 20)

    else:

        return np.random.uniform(1, 10)


def estimate_pledge():

    return np.random.uniform(0, 10)


def generate_ownership_data(df):

    print(
        "Generating institutional ownership analytics..."
    )

    ownership_data = []

    for _, row in df.iterrows():

        promoter = estimate_promoter_holding(
            row["SECTOR"]
        )

        fii = estimate_fii_holding(
            row["MARKET_CAP_CATEGORY"]
        )

        dii = estimate_dii_holding(
            row["MARKET_CAP_CATEGORY"]
        )

        pledge = estimate_pledge()

        ownership_data.append({

            "SYMBOL": row["SYMBOL"],

            "PROMOTER_HOLDING": round(
                promoter,
                2
            ),

            "FII_HOLDING": round(
                fii,
                2
            ),

            "DII_HOLDING": round(
                dii,
                2
            ),

            "PLEDGE_PERCENT": round(
                pledge,
                2
            )
        })

    return pd.DataFrame(
        ownership_data
    )


def main():

    print(
        "Loading institutional fundamentals..."
    )

    df = pd.read_csv(INPUT_FILE)

    ownership_df = generate_ownership_data(
        df
    )

    os.makedirs(
        "data/ownership",
        exist_ok=True
    )

    ownership_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nOwnership dataset generated\n")

    print(
        ownership_df.head()
    )

    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":

    main()