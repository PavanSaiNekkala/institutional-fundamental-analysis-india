def classify_sector(
    sector,
    industry
):

    # =====================================
    # SAFE LOWERCASE
    # =====================================

    sector = str(
        sector
    ).lower()

    industry = str(
        industry
    ).lower()

    text = (
        sector + " " + industry
    )

    # =====================================
    # BANKING & FINANCIALS
    # =====================================

    if any(keyword in text for keyword in [

        "bank",
        "financial",
        "finance",
        "insurance",
        "nbfc",
        "capital",
        "asset management",
        "broking"

    ]):

        return "Financial Services"

    # =====================================
    # INFORMATION TECHNOLOGY
    # =====================================

    elif any(keyword in text for keyword in [

        "software",
        "it services",
        "technology",
        "cloud",
        "ai",
        "analytics",
        "digital",
        "saas"

    ]):

        return "Information Technology"

    # =====================================
    # PHARMA
    # =====================================

    elif any(keyword in text for keyword in [

        "pharma",
        "pharmaceutical",
        "healthcare",
        "hospital",
        "biotech",
        "drug",
        "life sciences"

    ]):

        return "Healthcare"

    # =====================================
    # FMCG
    # =====================================

    elif any(keyword in text for keyword in [

        "fmcg",
        "consumer",
        "foods",
        "beverages",
        "household",
        "personal products"

    ]):

        return "Consumer Goods"

    # =====================================
    # AUTO
    # =====================================

    elif any(keyword in text for keyword in [

        "auto",
        "automobile",
        "vehicle",
        "tyre",
        "motor"

    ]):

        return "Automobile"

    # =====================================
    # ENERGY
    # =====================================

    elif any(keyword in text for keyword in [

        "oil",
        "gas",
        "energy",
        "power",
        "renewable",
        "solar",
        "electric"

    ]):

        return "Energy"

    # =====================================
    # METALS
    # =====================================

    elif any(keyword in text for keyword in [

        "steel",
        "metal",
        "mining",
        "copper",
        "aluminium",
        "iron"

    ]):

        return "Metals & Mining"

    # =====================================
    # REAL ESTATE
    # =====================================

    elif any(keyword in text for keyword in [

        "real estate",
        "construction",
        "cement",
        "infrastructure",
        "housing"

    ]):

        return "Infrastructure & Realty"

    # =====================================
    # TELECOM
    # =====================================

    elif any(keyword in text for keyword in [

        "telecom",
        "communication",
        "wireless",
        "broadband"

    ]):

        return "Telecommunication"

    # =====================================
    # CHEMICALS
    # =====================================

    elif any(keyword in text for keyword in [

        "chemical",
        "fertilizer",
        "agrochemical",
        "speciality chemical"

    ]):

        return "Chemicals"

    # =====================================
    # TEXTILES
    # =====================================

    elif any(keyword in text for keyword in [

        "textile",
        "garment",
        "fabric",
        "cotton"

    ]):

        return "Textiles"

    # =====================================
    # DEFAULT
    # =====================================

    return "Others"
