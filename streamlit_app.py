import streamlit as st
import pandas as pd
import plotly.express as px
import os


st.set_page_config(
    page_title="Institutional Fundamental Analysis",
    layout="wide"
)


# =====================================================
# CREATE DEMO DATA IF FILES DON'T EXIST
# =====================================================

def create_demo_data():

    os.makedirs("data/exports", exist_ok=True)

    demo_df = pd.DataFrame({

        "FINAL_RANK": [1, 2, 3, 4, 5],

        "SYMBOL": [
            "TCS",
            "HAL",
            "HDFCBANK",
            "INFY",
            "BEL"
        ],

        "SECTOR": [
            "IT",
            "DEFENCE",
            "BANKING",
            "IT",
            "DEFENCE"
        ],

        "GROWTH_SCORE": [85, 80, 75, 82, 78],

        "QUALITY_SCORE": [90, 88, 86, 84, 83],

        "OWNERSHIP_SCORE": [80, 79, 85, 76, 74],

        "FINAL_SCORE": [86, 82, 81, 80, 78],

        "RATING": [
            "STRONG BUY",
            "STRONG BUY",
            "BUY",
            "BUY",
            "BUY"
        ],

        "ROE": [0.42, 0.31, 0.18, 0.29, 0.24],

        "REVENUE_GROWTH": [0.18, 0.22, 0.14, 0.17, 0.19],

        "EARNINGS_GROWTH": [0.20, 0.24, 0.15, 0.18, 0.21]
    })

    sector_df = pd.DataFrame({

        "SECTOR": [
            "IT",
            "DEFENCE",
            "BANKING"
        ],

        "FINAL_SCORE": [82, 80, 75],

        "SECTOR_STATUS": [
            "LEADING",
            "LEADING",
            "STRONG"
        ]
    })

    demo_df.to_csv(
        "data/exports/final_rankings.csv",
        index=False
    )

    demo_df.to_csv(
        "data/exports/compounders.csv",
        index=False
    )

    demo_df.to_csv(
        "data/exports/institutional_buying.csv",
        index=False
    )

    sector_df.to_csv(
        "data/exports/sector_rotation.csv",
        index=False
    )


# =====================================================
# CHECK FILES
# =====================================================

required_files = [

    "data/exports/final_rankings.csv",

    "data/exports/compounders.csv",

    "data/exports/institutional_buying.csv",

    "data/exports/sector_rotation.csv"
]


missing = any(
    not os.path.exists(file)
    for file in required_files
)

if missing:

    create_demo_data()


# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    rankings = pd.read_csv(
        "data/exports/final_rankings.csv"
    )

    compounders = pd.read_csv(
        "data/exports/compounders.csv"
    )

    institutional = pd.read_csv(
        "data/exports/institutional_buying.csv"
    )

    sectors = pd.read_csv(
        "data/exports/sector_rotation.csv"
    )

    return rankings, compounders, institutional, sectors


rankings, compounders, institutional, sectors = load_data()


# =====================================================
# HEADER
# =====================================================

st.title("🇮🇳 Institutional Fundamental Analysis Platform")

st.markdown("""
Professional Indian Equity Institutional Analytics System
""")


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Filters")

selected_sector = st.sidebar.selectbox(
    "Sector",
    ["ALL"] + sorted(
        rankings["SECTOR"].dropna().unique().tolist()
    )
)

selected_rating = st.sidebar.selectbox(
    "Rating",
    ["ALL"] + sorted(
        rankings["RATING"].dropna().unique().tolist()
    )
)


# =====================================================
# FILTERS
# =====================================================

filtered_rankings = rankings.copy()

if selected_sector != "ALL":

    filtered_rankings = filtered_rankings[
        filtered_rankings["SECTOR"] == selected_sector
    ]

if selected_rating != "ALL":

    filtered_rankings = filtered_rankings[
        filtered_rankings["RATING"] == selected_rating
    ]


# =====================================================
# METRICS
# =====================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Stocks",
    len(filtered_rankings)
)

col2.metric(
    "Average Score",
    round(filtered_rankings["FINAL_SCORE"].mean(), 2)
)

col3.metric(
    "Top Sector",
    sectors.iloc[0]["SECTOR"]
)

col4.metric(
    "Best Rating",
    filtered_rankings["RATING"].mode()[0]
)


# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 Rankings",
    "💎 Compounders",
    "🏦 Institutional Buying",
    "📊 Sector Analytics"
])


# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader("Institutional Rankings")

    st.dataframe(
        filtered_rankings,
        use_container_width=True
    )

    fig = px.bar(
        filtered_rankings,
        x="SYMBOL",
        y="FINAL_SCORE",
        color="RATING",
        title="Top Institutional Picks"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader("Compounders")

    st.dataframe(
        compounders,
        use_container_width=True
    )


# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader("Institutional Buying")

    st.dataframe(
        institutional,
        use_container_width=True
    )


# =====================================================
# TAB 4
# =====================================================

with tab4:

    st.subheader("Sector Rotation")

    st.dataframe(
        sectors,
        use_container_width=True
    )

    fig2 = px.bar(
        sectors,
        x="SECTOR",
        y="FINAL_SCORE",
        color="SECTOR_STATUS",
        title="Sector Leadership"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Institutional Fundamental Analysis Platform | India"
)
