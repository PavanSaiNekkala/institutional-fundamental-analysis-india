import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Institutional Fundamental Analysis",
    layout="wide"
)


# =========================
# LOAD DATA
# =========================

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


# =========================
# HEADER
# =========================

st.title("🇮🇳 Institutional Fundamental Analysis Platform")

st.markdown("""
Professional Indian Equity Institutional Analytics System
""")


# =========================
# SIDEBAR
# =========================

st.sidebar.header("Dashboard Filters")

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


# =========================
# FILTER DATA
# =========================

filtered_rankings = rankings.copy()

if selected_sector != "ALL":

    filtered_rankings = filtered_rankings[
        filtered_rankings["SECTOR"] == selected_sector
    ]

if selected_rating != "ALL":

    filtered_rankings = filtered_rankings[
        filtered_rankings["RATING"] == selected_rating
    ]


# =========================
# TOP METRICS
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Stocks",
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
    "Top Rating",
    filtered_rankings["RATING"].mode()[0]
)


# =========================
# TABS
# =========================

tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 Rankings",
    "💎 Compounders",
    "🏦 Institutional Buying",
    "📊 Sector Analytics"
])


# =========================
# TAB 1 — RANKINGS
# =========================

with tab1:

    st.subheader("Institutional Rankings")

    display_columns = [
        "FINAL_RANK",
        "SYMBOL",
        "SECTOR",
        "FINAL_SCORE",
        "RATING",
        "GROWTH_SCORE",
        "QUALITY_SCORE",
        "OWNERSHIP_SCORE"
    ]

    st.dataframe(
        filtered_rankings[display_columns],
        use_container_width=True
    )

    fig = px.bar(
        filtered_rankings.head(10),
        x="SYMBOL",
        y="FINAL_SCORE",
        color="RATING",
        title="Top Institutional Picks"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================
# TAB 2 — COMPOUNDERS
# =========================

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

    st.dataframe(
        compounders[compounder_columns],
        use_container_width=True
    )

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


# =========================
# TAB 3 — INSTITUTIONAL
# =========================

with tab3:

    st.subheader("Institutional Accumulation")

    institutional_columns = [
        "INSTITUTIONAL_RANK",
        "SYMBOL",
        "SECTOR",
        "OWNERSHIP_SCORE",
        "FINAL_SCORE",
        "RATING"
    ]

    st.dataframe(
        institutional[institutional_columns],
        use_container_width=True
    )

    fig3 = px.bar(
        institutional.head(10),
        x="SYMBOL",
        y="OWNERSHIP_SCORE",
        color="SECTOR",
        title="Smart Money Accumulation"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )


# =========================
# TAB 4 — SECTOR ANALYTICS
# =========================

with tab4:

    st.subheader("Sector Rotation Analysis")

    st.dataframe(
        sectors,
        use_container_width=True
    )

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


# =========================
# FOOTER
# =========================

st.markdown("---")

st.caption(
    "Institutional Fundamental Analysis Platform | India"
)
