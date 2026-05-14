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

        df = df.replace(
            [np.inf, -np.inf],
            np.nan
        )

        df = df.drop_duplicates()

        if "MARKET_CAP" in df.columns:

            df = df[
                df["MARKET_CAP"] > 0
            ]

        if "FINAL_SCORE" in df.columns:

            df = df[
                df["FINAL_SCORE"].notna()
            ]

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

st.markdown(
    f"""
    ## 📊 Market Regime:
    `{market_regime}`
    """
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

subsector_filter = st.sidebar.multiselect(
    "Subsector",
    sorted(
        df["SUBSECTOR"]
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

elite_only = st.sidebar.checkbox(
    "Elite Stocks Only"
)

compounder_only = st.sidebar.checkbox(
    "Compounders Only"
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
# FILTERING
# =========================================================

filtered_df = df.copy()

if sector_filter:

    filtered_df = filtered_df[
        filtered_df["SECTOR"]
        .isin(sector_filter)
    ]

if subsector_filter:

    filtered_df = filtered_df[
        filtered_df["SUBSECTOR"]
        .isin(subsector_filter)
    ]

if trade_filter:

    filtered_df = filtered_df[
        filtered_df[
            "TRADE_DECISION"
        ]
        .isin(trade_filter)
    ]

if elite_only:

    filtered_df = filtered_df[
        filtered_df[
            "ELITE_FLAG"
        ] == 1
    ]

if compounder_only:

    filtered_df = filtered_df[
        filtered_df[
            "COMPOUNDER_FLAG"
        ] == 1
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
# KPI PANEL
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Stocks",
    len(filtered_df)
)

col2.metric(
    "Elite Stocks",
    int(
        filtered_df[
            "ELITE_FLAG"
        ].sum()
    )
)

col3.metric(
    "Avg Final Score",
    round(
        filtered_df[
            "FINAL_SCORE"
        ].mean(),
        2
    )
)

col4.metric(
    "Compounders",
    int(
        filtered_df[
            "COMPOUNDER_FLAG"
        ].sum()
    )
)

# =========================================================
# LEADERBOARD
# =========================================================

st.subheader(
    "🏆 Institutional Leaderboard"
)

leaderboard_columns = [

    "RANK",
    "SYMBOL",
    "SECTOR",
    "SUBSECTOR",
    "FINAL_SCORE",
    "CONFIDENCE_SCORE",
    "LEADERSHIP_SCORE",
    "TRADE_DECISION",
    "INSTITUTIONAL_GRADE",
    "CURRENT_PRICE"
]

available_columns = [

    col for col in leaderboard_columns
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
# SECTOR ROTATION
# =========================================================

st.subheader(
    "📊 Sector Rotation"
)

sector_strength = (

    filtered_df

    .groupby("SECTOR")[
        "FINAL_SCORE"
    ]

    .mean()

    .sort_values(
        ascending=False
    )

)

fig_sector = px.bar(

    sector_strength,

    title="Sector Strength",

    height=500

)

st.plotly_chart(
    fig_sector,
    use_container_width=True
)

# =========================================================
# SUBSECTOR STRENGTH
# =========================================================

st.subheader(
    "🔥 Subsector Strength"
)

subsector_strength = (

    filtered_df

    .groupby("SUBSECTOR")[
        "FINAL_SCORE"
    ]

    .mean()

    .sort_values(
        ascending=False
    )

    .head(25)

)

fig_subsector = px.bar(

    subsector_strength,

    title="Top Subsectors",

    height=600

)

st.plotly_chart(
    fig_subsector,
    use_container_width=True
)

# =========================================================
# ELITE STOCKS
# =========================================================

st.subheader(
    "🏆 Elite Institutional Stocks"
)

elite_df = filtered_df[

    filtered_df[
        "ELITE_FLAG"
    ] == 1

]

st.dataframe(

    elite_df[
        [
            "RANK",
            "SYMBOL",
            "SECTOR",
            "SUBSECTOR",
            "FINAL_SCORE",
            "CONFIDENCE_SCORE",
            "TRADE_DECISION"
        ]
    ],

    use_container_width=True
)

# =========================================================
# COMPOUNDER TRACKER
# =========================================================

st.subheader(
    "📈 Compounder Tracker"
)

compounders = filtered_df[

    filtered_df[
        "COMPOUNDER_FLAG"
    ] == 1

]

fig_compounders = px.scatter(

    compounders,

    x="QUALITY_SCORE",

    y="GROWTH_SCORE",

    size="MARKET_CAP",

    color="SECTOR",

    hover_name="SYMBOL",

    title="Compounder Universe"

)

st.plotly_chart(
    fig_compounders,
    use_container_width=True
)

# =========================================================
# INSTITUTIONAL LEADERSHIP
# =========================================================

st.subheader(
    "🚀 Institutional Leadership"
)

leaders = (

    filtered_df

    .sort_values(
        by="LEADERSHIP_SCORE",
        ascending=False
    )

    .head(20)

)

st.dataframe(

    leaders[
        [
            "SYMBOL",
            "SECTOR",
            "SUBSECTOR",
            "LEADERSHIP_SCORE",
            "CONFIDENCE_SCORE",
            "FINAL_SCORE"
        ]
    ],

    use_container_width=True
)

# =========================================================
# TREEMAP
# =========================================================

st.subheader(
    "🌐 Institutional Market Treemap"
)

fig_tree = px.treemap(

    filtered_df,

    path=[
        "SECTOR",
        "SUBSECTOR",
        "SYMBOL"
    ],

    values="MARKET_CAP",

    color="FINAL_SCORE",

    hover_data=[
        "TRADE_DECISION",
        "CONFIDENCE_SCORE"
    ]
)

st.plotly_chart(
    fig_tree,
    use_container_width=True
)

# =========================================================
# SCORE DISTRIBUTION
# =========================================================

st.subheader(
    "🧠 Institutional Score Distribution"
)

fig_hist = px.histogram(

    filtered_df,

    x="FINAL_SCORE",

    nbins=40

)

st.plotly_chart(
    fig_hist,
    use_container_width=True
)

# =========================================================
# TRADE BREAKDOWN
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
# INSTITUTIONAL GRADES
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
# DOWNLOAD
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
