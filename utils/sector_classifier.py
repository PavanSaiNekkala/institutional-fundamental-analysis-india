def classify_sector(sector_name, industry_name):

    sector_name = str(sector_name).upper()

    industry_name = str(industry_name).upper()


    # =====================================
    # IT
    # =====================================

    if (
        "SOFTWARE" in industry_name or
        "IT" in sector_name or
        "TECHNOLOGY" in sector_name
    ):

        return "IT"


    # =====================================
    # BANKING
    # =====================================

    elif (
        "BANK" in industry_name or
        "BANK" in sector_name
    ):

        return "BANKING"


    # =====================================
    # NBFC
    # =====================================

    elif (
        "FINANCE" in industry_name or
        "NBFC" in industry_name
    ):

        return "NBFC"


    # =====================================
    # PHARMA
    # =====================================

    elif (
        "PHARMA" in industry_name or
        "HEALTHCARE" in sector_name or
        "DRUG" in industry_name
    ):

        return "PHARMA"


    # =====================================
    # AUTO
    # =====================================

    elif (
        "AUTO" in industry_name or
        "AUTOMOBILE" in sector_name
    ):

        return "AUTO"


    # =====================================
    # FMCG
    # =====================================

    elif (
        "FMCG" in sector_name or
        "CONSUMER" in sector_name or
        "HOUSEHOLD" in industry_name
    ):

        return "FMCG"


    # =====================================
    # POWER
    # =====================================

    elif (
        "POWER" in industry_name or
        "UTILITY" in sector_name or
        "ENERGY" in sector_name
    ):

        return "POWER"


    # =====================================
    # DEFENCE
    # =====================================

    elif (
        "DEFENCE" in industry_name or
        "AEROSPACE" in industry_name
    ):

        return "DEFENCE"


    # =====================================
    # METALS
    # =====================================

    elif (
        "STEEL" in industry_name or
        "METAL" in sector_name
    ):

        return "METALS"


    # =====================================
    # REALTY
    # =====================================

    elif (
        "REAL ESTATE" in industry_name or
        "REALTY" in sector_name
    ):

        return "REALTY"


    # =====================================
    # CHEMICALS
    # =====================================

    elif (
        "CHEMICAL" in industry_name
    ):

        return "CHEMICALS"


    # =====================================
    # CAPITAL GOODS
    # =====================================

    elif (
        "INDUSTRIAL" in sector_name or
        "ENGINEERING" in industry_name
    ):

        return "CAPITAL GOODS"


    # =====================================
    # TELECOM
    # =====================================

    elif (
        "TELECOM" in industry_name
    ):

        return "TELECOM"


    # =====================================
    # DEFAULT
    # =====================================

    return "OTHERS"
