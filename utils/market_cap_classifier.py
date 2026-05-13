def classify_market_cap(
    market_cap
):

    # =====================================
    # HANDLE MISSING VALUES
    # =====================================

    try:

        market_cap = float(
            market_cap
        )

    except Exception:

        return "UNKNOWN"

    # =====================================
    # NEGATIVE / INVALID
    # =====================================

    if market_cap <= 0:

        return "UNKNOWN"

    # =====================================
    # INDIAN MARKET CAP CLASSIFICATION
    # =====================================

    # 1 Crore = 10,000,000

    # ---------------------------------
    # MEGA CAP
    # > 200000 Cr
    # ---------------------------------

    if market_cap >= 2_000_000_000_000:

        return "MEGA CAP"

    # ---------------------------------
    # LARGE CAP
    # 50000 Cr - 200000 Cr
    # ---------------------------------

    elif market_cap >= 500_000_000_000:

        return "LARGE CAP"

    # ---------------------------------
    # MID CAP
    # 10000 Cr - 50000 Cr
    # ---------------------------------

    elif market_cap >= 100_000_000_000:

        return "MID CAP"

    # ---------------------------------
    # SMALL CAP
    # 1000 Cr - 10000 Cr
    # ---------------------------------

    elif market_cap >= 10_000_000_000:

        return "SMALL CAP"

    # ---------------------------------
    # MICRO CAP
    # Below 1000 Cr
    # ---------------------------------

    else:

        return "MICRO CAP"
