# =========================================================
# INSTITUTIONAL SECTOR TAXONOMY
# =========================================================

SECTOR_TAXONOMY = {

    # =====================================================
    # FINANCIALS
    # =====================================================

    "Financials": [

        "Private Sector Banks",
        "PSU Banks",
        "Small Finance Banks",
        "NBFC – Lending",
        "NBFC – Investment",
        "Housing Finance",
        "Microfinance",
        "Life Insurance",
        "General Insurance",
        "Asset Management Companies",
        "Stock Broking & Exchanges"
    ],

    # =====================================================
    # TECHNOLOGY
    # =====================================================

    "Technology": [

        "IT Services",
        "Software Products",
        "SaaS",
        "IT Consulting",
        "Cloud Services",
        "Cybersecurity",
        "Data Analytics / AI"
    ],

    # =====================================================
    # INDUSTRIALS
    # =====================================================

    "Industrials": [

        "Capital Goods",
        "Engineering & EPC",
        "Industrial Machinery",
        "Industrial Automation",
        "Electrical Equipment",
        "Heavy Electricals",
        "Construction & Infrastructure"
    ],

    # =====================================================
    # AUTOMOBILES
    # =====================================================

    "Automobiles": [

        "Passenger Vehicles",
        "Commercial Vehicles",
        "Two & Three Wheelers",
        "Auto Components",
        "Tyres & Rubber",
        "EV Manufacturers",
        "EV Components"
    ],

    # =====================================================
    # ENERGY
    # =====================================================

    "Energy": [

        "Oil Exploration",
        "Oil Refining",
        "Oil Marketing",
        "Gas Transmission",
        "Gas Distribution",
        "Power Generation – Thermal",
        "Power Generation – Renewable",
        "Power Transmission",
        "Power Distribution"
    ],

    # =====================================================
    # METALS
    # =====================================================

    "Metals": [

        "Iron & Steel",
        "Aluminium",
        "Copper",
        "Mining & Minerals",
        "Coal"
    ],

    # =====================================================
    # CHEMICALS
    # =====================================================

    "Chemicals": [

        "Commodity Chemicals",
        "Specialty Chemicals",
        "Petrochemicals",
        "Agrochemicals",
        "Fertilizers",
        "Paints & Coatings"
    ],

    # =====================================================
    # HEALTHCARE
    # =====================================================

    "Healthcare": [

        "Pharma – Formulations",
        "Pharma – API",
        "Hospitals",
        "Diagnostics",
        "Biotechnology",
        "Medical Devices"
    ],

    # =====================================================
    # CONSUMER
    # =====================================================

    "Consumer": [

        "FMCG – Food",
        "FMCG – Personal Care",
        "FMCG – Beverages",
        "Tobacco",
        "Durables – Appliances",
        "Durables – Electronics"
    ],

    # =====================================================
    # RETAIL
    # =====================================================

    "Retail": [

        "Retail – Grocery",
        "Retail – Apparel",
        "Retail – Electronics",
        "E-commerce"
    ],

    # =====================================================
    # TEXTILES
    # =====================================================

    "Textiles": [

        "Cotton Textiles",
        "Synthetic Textiles",
        "Garments",
        "Home Textiles"
    ],

    # =====================================================
    # REAL ESTATE
    # =====================================================

    "Real Estate": [

        "Residential",
        "Commercial",
        "Construction"
    ],

    # =====================================================
    # BUILDING MATERIALS
    # =====================================================

    "Building Materials": [

        "Cement",
        "Pipes",
        "Tiles",
        "Plywood"
    ],

    # =====================================================
    # LOGISTICS
    # =====================================================

    "Logistics": [

        "Logistics Services",
        "Warehousing",
        "Shipping",
        "Ports",
        "Aviation",
        "Railways"
    ],

    # =====================================================
    # TELECOM
    # =====================================================

    "Telecom": [

        "Telecom Services",
        "Telecom Infra"
    ],

    # =====================================================
    # MEDIA
    # =====================================================

    "Media": [

        "Broadcasting",
        "Print Media",
        "Digital Media"
    ],

    # =====================================================
    # HOSPITALITY
    # =====================================================

    "Hospitality": [

        "Hotels",
        "Restaurants",
        "Travel"
    ],

    # =====================================================
    # AGRICULTURE
    # =====================================================

    "Agriculture": [

        "Seeds",
        "Fertilizers",
        "Sugar",
        "Dairy",
        "Tea & Coffee"
    ],

    # =====================================================
    # DEFENCE
    # =====================================================

    "Defence": [

        "Defence Equipment",
        "Aerospace",
        "Shipbuilding"
    ],

    # =====================================================
    # PACKAGING
    # =====================================================

    "Packaging": [

        "Packaging",
        "Paper",
        "Plastics",
        "Glass"
    ],

    # =====================================================
    # JEWELLERY
    # =====================================================

    "Jewellery": [

        "Jewellery Retail",
        "Diamond Processing"
    ],

    # =====================================================
    # SERVICES
    # =====================================================

    "Services": [

        "Education",
        "Business Services"
    ],

    # =====================================================
    # EMERGING
    # =====================================================

    "Emerging": [

        "EV Ecosystem",
        "Battery",
        "Renewable Equipment",
        "Recycling"
    ],

    # =====================================================
    # MISC
    # =====================================================

    "Misc": [

        "Printing",
        "Diversified",
        "Industrial Services"
    ]
}

# =========================================================
# REVERSE LOOKUP
# =========================================================

SUBSECTOR_TO_SECTOR = {}

for sector, subsectors in (
    SECTOR_TAXONOMY.items()
):

    for subsector in subsectors:

        SUBSECTOR_TO_SECTOR[
            subsector
        ] = sector
