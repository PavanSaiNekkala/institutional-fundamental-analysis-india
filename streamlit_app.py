import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Institutional Fundamental Analysis",
    layout="wide"
)


@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/exports/final_rankings.csv"
    )

    return df


df = load_data()


# TITLE

st.title("🇮🇳 Institutional Fundamental Analysis Platform")

st.markdown("""
Institutional-grade Indian equity research dashboard
""")


# SIDEBAR FILTERS

st.sidebar.header("Filters")

selected_sector = st.sidebar.selectbox(
    "Select Sector",
    ["ALL"] + sorted(df["SECTOR"].dropna().unique().tolist())
)

selected_rating = st.sidebar.selectbox(
    "Select Rating",
    ["ALL"] + sorted(df["RATING"].dropna().unique().tolist())
)


# FILTERING

filtered_df = df.copy()

if selected_sector != "ALL":

    filtered_df = filtered_df[
        filtered_df["SECTOR"] == selected_sector
    ]

if selected_rating != "ALL":

    filtered_df = filtered_df[
        filtered_df["RATING"] == selected_rating
    ]


# METRICS

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Stocks",
    len(filtered_df)
)

col2.metric(
    "Average Score",
    round(filtered_df["FINAL_SCORE"].mean(), 2)
)

col3.metric(
    "Top Rating",
    filtered_df["RATING"].mode()[0]
)


# TOP STOCKS TABLE

st.subheader("🏆 Institutional Rankings")

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
    filtered_df[display_columns],
    use_container_width=True
)


# SCORE DISTRIBUTION

st.subheader("📊 Institutional Score Distribution")

fig = px.histogram(
    filtered_df,
    x="FINAL_SCORE",
    nbins=20,
    title="Final Score Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# TOP STOCKS CHART

st.subheader("🚀 Top Institutional Picks")

top_10 = filtered_df.sort_values(
    by="FINAL_SCORE",
    ascending=False
).head(10)

fig2 = px.bar(
    top_10,
    x="SYMBOL",
    y="FINAL_SCORE",
    color="RATING",
    title="Top Ranked Stocks"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# FOOTER

st.markdown("---")

st.caption(
    "Institutional Fundamental Analysis Platform | India"
)
