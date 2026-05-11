import streamlit as st
import pandas as pd
import plotly.express as px
import os


st.set_page_config(
    page_title="Institutional Fundamental Analysis",
    layout="wide"
)


# =====================================================
# REQUIRED FILE CHECK
# =====================================================

required_files = [

    "data/exports/final_rankings.csv",

    "data/exports/compounders.csv",

    "data/exports/institutional_buying.csv",

    "data/exports/sector_rotation.csv"
]


missing_files = [

    file for file in required_files
    if not os.path.exists(file)
]


if missing_files:

    st.error(
        "Required institutional datasets are missing."
    )

    st.info(
        "Run the institutional data pipeline first."
    )

    st.code("""
python collectors/screener_collector.py
python preprocessing/cleaner.py
python scoring/growth_score.py
python scoring/quality_score.py
python scoring/ownership_score.py
python scoring/valuation_score.py
python scoring/final_ranker.py
python analytics/compounder_detector.py
python analytics/institutional_buying.py
python analytics/sector_rotation.py
    """)

    st.stop()


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
# SIDEBAR FILTERS
# =====================================================

st.sidebar.title("Filters")

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
# FILTER DATA
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
# HEADER
# =====================================================

st.title(
    "🇮🇳 Institutional Fundamental Analysis Platform"
)

st.markdown(
    "Professional Indian Equity Institutional Analytics System"
)


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
# TAB 1 — RANKINGS
# =====================================================

with tab1:

    st.subheader("Institutional Rankings")

    ranking_columns = [

        "FINAL_RANK",

        "SYMBOL",

        "SECTOR",

        "FINAL_SCORE",

        "RATING",

        "GROWTH_SCORE",

        "QUALITY_SCORE",

        "OWNERSHIP_SCORE",

        "VALUATION_SCORE"
    ]

    available_columns = [
        col for col in ranking_columns
        if col in filtered_rankings.columns
    ]

    st.dataframe(
        filtered_rankings[available_columns],
        use_container_width=True
    )

    top_rankings = filtered_rankings.sort_values(
        by="FINAL_SCORE",
        ascending=False
    ).head(10)

    fig1 = px.bar(
        top_rankings,
        x="SYMBOL",
        y="FINAL_SCORE",
        color="RATING",
        title="Top Institutional Picks"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )


# =====================================================
# TAB 2 — COMPOUNDERS
# =====================================================

with tab2:

    st.subheader("Long-Term Compounders")

    compounder_columns = [

        "COMPOUNDER_RANK",

        "SYMBOL",

        "SECTOR",

        "ROE",

        "REVENUE_GROWTH",

        "EARNINGS_GROWTH",

        "FINAL_SCORE",

        "RATING"
    ]

    available_compounder_columns = [
        col for col in compounder_columns
        if col in compounders.columns
    ]

    st.dataframe(
        compounders[
            available_compounder_columns
        ],
        use_container_width=True
    )

    if "ROE" in compounders.columns:

        fig2 = px.scatter(
            compounders,
            x="ROE",
            y="FINAL_SCORE",
            color="SECTOR",
            size="FINAL_SCORE",
            hover_data=["SYMBOL"],
            title="Compounder Quality Map"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )


# =====================================================
# TAB 3 — INSTITUTIONAL BUYING
# =====================================================

with tab3:

    st.subheader("Institutional Accumulation")

    institutional_columns = [

        "INSTITUTIONAL_RANK",

        "SYMBOL",

        "SECTOR",

        "PROMOTER_HOLDING",

        "FII_HOLDING",

        "DII_HOLDING",

        "OWNERSHIP_SCORE",

        "FINAL_SCORE",

        "RATING"
    ]

    available_institutional_columns = [
        col for col in institutional_columns
        if col in institutional.columns
    ]

    st.dataframe(
        institutional[
            available_institutional_columns
        ],
        use_container_width=True
    )

    if "OWNERSHIP_SCORE" in institutional.columns:

        top_inst = institutional.sort_values(
            by="OWNERSHIP_SCORE",
            ascending=False
        ).head(10)

        fig3 = px.bar(
            top_inst,
            x="SYMBOL",
            y="OWNERSHIP_SCORE",
            color="SECTOR",
            title="Smart Money Accumulation"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )


# =====================================================
# TAB 4 — SECTOR ANALYTICS
# =====================================================

with tab4:

    st.subheader("Sector Rotation Analysis")

    st.dataframe(
        sectors,
        use_container_width=True
    )

    if "SECTOR_STATUS" in sectors.columns:

        fig4 = px.bar(
            sectors,
            x="SECTOR",
            y="FINAL_SCORE",
            color="SECTOR_STATUS",
            title="Sector Leadership Rankings"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )


# =====================================================
# SCORE DISTRIBUTION
# =====================================================

st.subheader("📈 Institutional Score Distribution")

fig5 = px.histogram(
    filtered_rankings,
    x="FINAL_SCORE",
    nbins=20,
    title="Final Institutional Score Distribution"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Institutional Fundamental Analysis Platform | India"
)
