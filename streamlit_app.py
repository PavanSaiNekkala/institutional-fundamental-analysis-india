import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
import traceback
from pathlib import Path

warnings.filterwarnings("ignore")

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Institutional Analytics Engine",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.metric-container {
    background-color: #1E1E1E;
    padding: 10px;
    border-radius: 10px;
}

.stDataFrame {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# FILE PATHS
# =========================================================

PARQUET_FILE = (
    "data/cache/parquet/"
    "institutional_rankings.parquet"
)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data(show_spinner=False)

def load_data():

    try:

        if not Path(PARQUET_FILE).exists():

            st.error(
                f"""
                Missing parquet dataset:

                {PARQUET_FILE}

                Run pipeline first.
                """
            )

            return pd.DataFrame()

        df = pd.read_parquet(PARQUET_FILE)

        # =====================================
        # DATA CLEANING
        # =====================================

        df = df.replace(
            [np.inf, -np.inf],
            np.nan
        )

        df = df.drop_duplicates()

        # Remove invalid market caps
        if "MARKET_CAP" in df.columns:

            df = df[
                df["MARKET_CAP"] > 0
            ]

        # Remove invalid scores
        if "FINAL_SCORE" in df.columns:

            df = df[
                df["FINAL_SCORE"].notna()
            ]

        # Sort rankings
        if "FINAL_SCORE" in df.columns:

            df = df.sort_values(
                by="FINAL_SCORE",
                ascending=False
            )

        return df

    except Exception as e:

        st.error(
            f"Error loading parquet:\n{e}"
        )

        traceback.print_exc()

        return pd.DataFrame()

# =========================================================
# LOAD DATAFRAME
# =========================================================

df = load_data()

if df.empty:

    st.stop()

# =========================================================
# HEADER
# =========================================================

st.title(
    "📈 Institutional Analytics Dashboard"
)

st.markdown(
    """
    Enterprise-grade institutional
    stock analysis and ranking platform
    """
)

# =========================================================
# MARKET REGIME
# =========================================================

market_regime = (
    df["MARKET_REGIME"].iloc[0]
    if "MARKET_REGIME" in df.columns
    else "UNKNOWN"
)

if market_regime == "BULLISH":

    st.success(
        f"🟢 Market Regime: {market_regime}"
    )

elif market_regime == "NEUTRAL":

    st.warning(
        f"🟡 Market Regime: {market_regime}"
    )

else:

    st.error(
        f"🔴 Market Regime: {market_regime}"
    )

# =========================================================
# METRICS
# =========================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(
        "Stocks",
        len(df)
    )

with col2:

    strong_buy_count = len(
        df[
            df["TRADE_DECISION"]
            == "INSTITUTIONAL STRONG BUY"
        ]
    )

    st.metric(
        "Strong Buy",
        strong_buy_count
    )

with col3:

    avg_score = round(
        df["FINAL_SCORE"].mean(),
        2
    )

    st.metric(
        "Average Score",
        avg_score
    )

with col4:

    top_score = round(
        df["FINAL_SCORE"].max(),
        2
    )

    st.metric(
        "Top Score",
        top_score
    )

with col5:

    sectors = (
        df["SECTOR"]
        .nunique()
        if "SECTOR" in df.columns
        else 0
    )

    st.metric(
        "Sectors",
        sectors
    )

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title(
    "⚙ Institutional Filters"
)

sector_filter = st.sidebar.multiselect(
    "Sector",
    sorted(
        df["SECTOR"]
        .dropna()
        .unique()
    )
)

market_cap_filter = st.sidebar.multiselect(
    "Market Cap Category",
    sorted(
        df[
            "MARKET_CAP_CATEGORY"
        ]
        .dropna()
        .unique()
    )
)

trade_filter = st.sidebar.multiselect(
    "Trade Decision",
    sorted(
        df[
            "TRADE_DECISION"
        ]
        .dropna()
        .unique()
    )
)

min_score = st.sidebar.slider(
    "Minimum Final Score",
    min_value=0,
    max_value=100,
    value=50
)

top_n = st.sidebar.slider(
    "Top N Stocks",
    min_value=10,
    max_value=500,
    value=100
)

search_stock = st.sidebar.text_input(
    "Search Symbol"
)
# =========================================================
# CONFIDENCE SCORE
# =========================================================

if "FINAL_SCORE" in df.columns:

    df["CONFIDENCE_SCORE"] = (
        (
            df["FINAL_SCORE"] * 0.60
        ) +
        (
            df["QUALITY_SCORE"] * 0.25
        ) +
        (
            df["OWNERSHIP_SCORE"] * 0.15
        )
    ).round(2)
# =========================================================
# FILTERS
# =========================================================

filtered_df = df.copy()

if sector_filter:

    filtered_df = filtered_df[
        filtered_df["SECTOR"]
        .isin(sector_filter)
    ]

if market_cap_filter:

    filtered_df = filtered_df[
        filtered_df[
            "MARKET_CAP_CATEGORY"
        ]
        .isin(market_cap_filter)
    ]

if trade_filter:

    filtered_df = filtered_df[
        filtered_df[
            "TRADE_DECISION"
        ]
        .isin(trade_filter)
    ]

filtered_df = filtered_df[
    filtered_df["FINAL_SCORE"]
    >= min_score
]

if search_stock:

    filtered_df = filtered_df[
        filtered_df["SYMBOL"]
        .astype(str)
        .str.contains(
            search_stock,
            case=False,
            na=False
        )
    ]

filtered_df = filtered_df.head(top_n)

# =========================================================
# TOP PICKS TABLE
# =========================================================

st.subheader(
    "🏆 Institutional Leaderboard"
)

columns_to_show = [

    "RANK",
    "SYMBOL",
    "FINAL_SCORE",
    "GROWTH_SCORE",
    "QUALITY_SCORE",
    "OWNERSHIP_SCORE",
    "TRADE_DECISION",
    "INSTITUTIONAL_GRADE",
    "MARKET_CAP_CATEGORY",
    "SECTOR",
    "CURRENT_PRICE"
]

available_columns = [

    col for col in columns_to_show
    if col in filtered_df.columns
]

st.dataframe(
    filtered_df[
        available_columns
    ],
    use_container_width=True,
    height=650
)

# =========================================================
# SCORE DISTRIBUTION
# =========================================================

st.subheader(
    "📊 Final Score Distribution"
)

fig = px.histogram(
    filtered_df,
    x="FINAL_SCORE",
    nbins=30,
    title="Institutional Score Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# TOP STOCKS CHART
# =========================================================

st.subheader(
    "🚀 Top Institutional Stocks"
)

chart_df = (
    filtered_df
    .sort_values(
        by="FINAL_SCORE",
        ascending=False
    )
    .head(20)
)

fig_top = px.bar(
    chart_df,
    x="SYMBOL",
    y="FINAL_SCORE",
    color="FINAL_SCORE",
    title="Top 20 Institutional Stocks"
)

st.plotly_chart(
    fig_top,
    use_container_width=True
)

# =========================================================
# SECTOR ANALYTICS
# =========================================================

st.subheader(
    "🏭 Sector Strength Analysis"
)

sector_scores = (
    filtered_df
    .groupby("SECTOR")["FINAL_SCORE"]
    .mean()
    .sort_values(ascending=False)
    .head(15)
)

fig_sector = px.bar(
    sector_scores,
    title="Top Sector Scores"
)

st.plotly_chart(
    fig_sector,
    use_container_width=True
)
# =========================================================
# MARKET CAP TREEMAP
# =========================================================

st.subheader(
    "🌐 Market Cap Treemap"
)

if (
    "MARKET_CAP" in filtered_df.columns
    and
    "SECTOR" in filtered_df.columns
):

    treemap_df = (
        filtered_df
        .sort_values(
            by="MARKET_CAP",
            ascending=False
        )
        .head(100)
    )

    fig_tree = px.treemap(
        treemap_df,
        path=["SECTOR", "SYMBOL"],
        values="MARKET_CAP",
        color="FINAL_SCORE",
        hover_data=[
            "FINAL_SCORE",
            "TRADE_DECISION"
        ]
    )

    st.plotly_chart(
        fig_tree,
        use_container_width=True
    )
# =========================================================
# TRADE DECISION BREAKDOWN
# =========================================================

st.subheader(
    "📌 Trade Decision Breakdown"
)

trade_counts = (
    filtered_df[
        "TRADE_DECISION"
    ]
    .value_counts()
)

fig_trade = px.pie(
    values=trade_counts.values,
    names=trade_counts.index,
    title="Trade Decision Distribution"
)

st.plotly_chart(
    fig_trade,
    use_container_width=True
)

# =========================================================
# INSTITUTIONAL GRADE
# =========================================================

st.subheader(
    "🏅 Institutional Grade Distribution"
)

grade_counts = (
    filtered_df[
        "INSTITUTIONAL_GRADE"
    ]
    .value_counts()
)

fig_grade = px.bar(
    x=grade_counts.index,
    y=grade_counts.values,
    title="Institutional Grades"
)

st.plotly_chart(
    fig_grade,
    use_container_width=True
)
# =========================================================
# HIGH CONFIDENCE STOCKS
# =========================================================

st.subheader(
    "🔥 Highest Confidence Stocks"
)

confidence_df = (
    filtered_df
    .sort_values(
        by="CONFIDENCE_SCORE",
        ascending=False
    )
    .head(15)
)

confidence_columns = [

    "SYMBOL",
    "FINAL_SCORE",
    "CONFIDENCE_SCORE",
    "TRADE_DECISION",
    "SECTOR"
]

available_confidence_columns = [

    col for col in confidence_columns
    if col in confidence_df.columns
]

st.dataframe(
    confidence_df[
        available_confidence_columns
    ],
    use_container_width=True
)
# =========================================================
# RAW DATA
# =========================================================

with st.expander(
    "🔍 View Raw Dataset"
):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

# =========================================================
# DOWNLOADS
# =========================================================

st.subheader(
    "⬇ Export Institutional Dataset"
)

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name=(
        "institutional_rankings.csv"
    ),
    mime="text/csv"
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    """
    Institutional Quant Research Platform
    | Built with Python + Streamlit + Plotly
    """
)
