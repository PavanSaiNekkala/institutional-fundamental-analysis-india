def classify_market_cap(market_cap):

    """
    Market cap values are in INR
    """

    if market_cap is None:

        return "UNKNOWN"


    # Convert to Crores
    market_cap_cr = market_cap / 10000000


    # =====================================
    # LARGE CAP
    # =====================================

    if market_cap_cr >= 20000:

        return "LARGE CAP"


    # =====================================
    # MID CAP
    # =====================================

    elif market_cap_cr >= 5000:

        return "MID CAP"


    # =====================================
    # SMALL CAP
    # =====================================

    elif market_cap_cr >= 500:

        return "SMALL CAP"


    # =====================================
    # MICRO CAP
    # =====================================

    else:

        return "MICRO CAP"
