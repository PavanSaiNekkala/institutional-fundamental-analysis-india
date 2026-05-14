import pandas as pd
import numpy as np

# =========================================================
# BREAKOUT ALERTS
# =========================================================

def breakout_alerts(df):

    breakout_df = df[

        (
            df["BREAKOUT_FLAG"] == 1
        )

        &

        (
            df[
                "AI_CONVICTION_SCORE"
            ] >= 80
        )
    ]

    alerts = []

    for _, row in breakout_df.iterrows():

        alerts.append({

            "TYPE":
                "BREAKOUT",

            "SYMBOL":
                row["SYMBOL"],

            "MESSAGE":
                (
                    f"{row['SYMBOL']} "
                    f"showing breakout characteristics"
                )
        })

    return alerts

# =========================================================
# SMART MONEY ALERTS
# =========================================================

def smart_money_alerts(df):

    smart_df = df[

        (
            df[
                "SMART_MONEY_SCORE"
            ] >= 80
        )
    ]

    alerts = []

    for _, row in smart_df.iterrows():

        alerts.append({

            "TYPE":
                "SMART_MONEY",

            "SYMBOL":
                row["SYMBOL"],

            "MESSAGE":
                (
                    f"Institutional accumulation "
                    f"detected in "
                    f"{row['SYMBOL']}"
                )
        })

    return alerts

# =========================================================
# CRASH RISK ALERTS
# =========================================================

def crash_risk_alerts(df):

    risk_df = df[

        (
            df[
                "CRASH_RISK_SCORE"
            ] >= 75
        )
    ]

    alerts = []

    for _, row in risk_df.iterrows():

        alerts.append({

            "TYPE":
                "CRASH_RISK",

            "SYMBOL":
                row["SYMBOL"],

            "MESSAGE":
                (
                    f"High crash risk "
                    f"detected in "
                    f"{row['SYMBOL']}"
                )
        })

    return alerts

# =========================================================
# ELITE ALERTS
# =========================================================

def elite_alerts(df):

    elite_df = df[

        (
            df["ELITE_FLAG"] == 1
        )

        &

        (
            df[
                "AI_CONVICTION_SCORE"
            ] >= 85
        )
    ]

    alerts = []

    for _, row in elite_df.iterrows():

        alerts.append({

            "TYPE":
                "ELITE",

            "SYMBOL":
                row["SYMBOL"],

            "MESSAGE":
                (
                    f"Elite institutional "
                    f"setup in "
                    f"{row['SYMBOL']}"
                )
        })

    return alerts

# =========================================================
# COMPOUNDER ALERTS
# =========================================================

def compounder_alerts(df):

    compounder_df = df[

        (
            df[
                "COMPOUNDER_PROBABILITY"
            ] >= 85
        )
    ]

    alerts = []

    for _, row in compounder_df.iterrows():

        alerts.append({

            "TYPE":
                "COMPOUNDER",

            "SYMBOL":
                row["SYMBOL"],

            "MESSAGE":
                (
                    f"High compounder probability "
                    f"in "
                    f"{row['SYMBOL']}"
                )
        })

    return alerts

# =========================================================
# SECTOR ROTATION ALERTS
# =========================================================

def sector_rotation_alerts(df):

    sector_strength = (

        df

        .groupby("SECTOR")[
            "FINAL_SCORE"
        ]

        .mean()

        .sort_values(
            ascending=False
        )
    )

    top_sector = (
        sector_strength.index[0]
    )

    return [{

        "TYPE":
            "SECTOR_ROTATION",

        "SYMBOL":
            top_sector,

        "MESSAGE":
            (
                f"Sector leadership shifting "
                f"towards {top_sector}"
            )
    }]

# =========================================================
# MARKET REGIME ALERT
# =========================================================

def market_regime_alert(df):

    regime = (
        df["MARKET_REGIME"]
        .iloc[0]
    )

    return [{

        "TYPE":
            "MARKET_REGIME",

        "SYMBOL":
            "MARKET",

        "MESSAGE":
            (
                f"Current market regime: "
                f"{regime}"
            )
    }]

# =========================================================
# MASTER ALERT ENGINE
# =========================================================

def generate_alerts(df):

    alerts = []

    alerts.extend(
        breakout_alerts(df)
    )

    alerts.extend(
        smart_money_alerts(df)
    )

    alerts.extend(
        crash_risk_alerts(df)
    )

    alerts.extend(
        elite_alerts(df)
    )

    alerts.extend(
        compounder_alerts(df)
    )

    alerts.extend(
        sector_rotation_alerts(df)
    )

    alerts.extend(
        market_regime_alert(df)
    )

    alerts_df = pd.DataFrame(alerts)

    return alerts_df
