SECTOR_MAP = {

    "BANKING": [
        "HDFCBANK",
        "ICICIBANK",
        "SBIN",
        "KOTAKBANK",
        "AXISBANK"
    ],

    "IT": [
        "TCS",
        "INFY",
        "WIPRO",
        "HCLTECH",
        "TECHM"
    ],

    "PHARMA": [
        "SUNPHARMA",
        "DRREDDY",
        "CIPLA",
        "DIVISLAB"
    ],

    "AUTO": [
        "MARUTI",
        "TATAMOTORS",
        "M&M",
        "BAJAJ-AUTO"
    ],

    "FMCG": [
        "HINDUNILVR",
        "ITC",
        "NESTLEIND",
        "BRITANNIA"
    ],

    "POWER": [
        "NTPC",
        "POWERGRID",
        "TATAPOWER",
        "ADANIPOWER"
    ],

    "DEFENCE": [
        "HAL",
        "BEL",
        "BDL",
        "MAZDOCK"
    ],

    "RAILWAYS": [
        "IRFC",
        "RVNL",
        "IRCON",
        "RAILTEL"
    ]
}


def get_sector(symbol):

    for sector, stocks in SECTOR_MAP.items():

        if symbol in stocks:
            return sector

    return "OTHERS"
