# Final Enterprise Streamlit Dashboard (`streamlit_app.py`)

```python
import streamlit as st
import pandas as pd
import numpy as np
import warnings
import traceback
from pathlib import Path

warnings.filterwarnings("ignore")

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Institutional Analytics Engine",
    page_icon="📈",
    layout="wide"
)

# =========================================
# FILE PATHS
# =========================================

PARQUET_FILE = (
    "data/cache/parquet/"
    "institutional_rankings.parquet"
)

# =========================================
# LOAD DATA
# =========================================

@st.cache_data

def load_data():

    try:

        if not Path(PARQUET_FILE).exists():

            st.error(
                f"Missing parquet file:\n{PARQUET_FILE}"
            )

            return pd.DataFrame()

        df = pd.read_parquet(
            PARQUET_FILE
        )

        return df

    except Exception as e:

        st.error(
            f"Error loading parquet:\n{e}"
        )

        traceback.print_exc()

        return pd.DataFrame()


# =========================================
# LOAD DATAFRAME
# =========================================

df = load_data()

if df.empty:

    st.stop()

# =========================================
# HEADER
# =========================================

st.title(
    "📈 Institutional Analytics Dashboard"
)

st.markdown(
    "Enterprise-grade institutional stock analysis engine"
)

# =========================================
# MARKET REGIME
# =========================================

market_regime = (
    df["MARKET_REGIME"]
    .iloc[0]
)

if market_regime == "BULLISH":

    st.success(
        f"Market Regime: {market_regime}"
    )

elif market_regime == "NEUTRAL":

    st.warning(
        f"Market Regime: {market_regime}"
    )

else:

    st.error(
        f"Market Regime: {market_regime}"
    )

# =========================================
# METRICS
# =========================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Stocks Analyzed",
        len(df)
    )

with col2:

    strong_buy_count = len(
        df[
            df[
                "TRADE_DECISION"
            ]
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

# =========================================
# SIDEBAR FILTERS
# =========================================

st.sidebar.header(
    "Institutional Filters"
)

sector_filter = st.sidebar.multiselect(
    "Sector",
    options=sorted(
        df["SECTOR"]
        .dropna()
        .unique()
    ),
    default=[]
)

market_cap_filter = (
    st.sidebar.multiselect(
        "Market Cap Category",
        options=sorted(
            df[
                "MARKET_CAP_CATEGORY"
            ]
            .dropna()
            .unique()
        ),
        default=[]
    )
)

trade_filter = st.sidebar.multiselect(
    "Trade Decision",
    options=sorted(
        df[
            "TRADE_DECISION"
        ]
        .dropna()
        .unique()
    ),
    default=[]
)

min_score = st.sidebar.slider(
    "Minimum Final Score",
    min_value=0,
    max_value=100,
    value=40
)

search_stock = st.sidebar.text_input(
    "Search Symbol"
)

# =========================================
# APPLY FILTERS
# =========================================

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
    filtered_df[
        "FINAL_SCORE"
    ] >= min_score
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

# =========================================
# TOP PICKS
# =========================================

st.subheader(
    "🏆 Top Institutional Picks"
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
    height=600
)

# =========================================
# TOP 20 CHART
# =========================================

st.subheader(
    "📊 Top 20 Institutional Stocks"
)

chart_df = (
    filtered_df
    .sort_values(
        by="FINAL_SCORE",
        ascending=False
    )
    .head(20)
)

if not chart_df.empty:

    st.bar_chart(
        data=chart_df.set_index(
            "SYMBOL"
        )[
            "FINAL_SCORE"
        ]
    )

# =========================================
# SECTOR DISTRIBUTION
# =========================================

st.subheader(
    "🏭 Sector Distribution"
)

sector_counts = (
    filtered_df["SECTOR"]
    .value_counts()
    .head(15)
)

if not sector_counts.empty:

    st.bar_chart(
        sector_counts
    )

# =========================================
# TRADE DECISION BREAKDOWN
# =========================================

st.subheader(
    "📌 Trade Decision Breakdown"
)

trade_counts = (
    filtered_df[
        "TRADE_DECISION"
    ]
    .value_counts()
)

st.dataframe(
    trade_counts,
    use_container_width=True
)

# =========================================
# INSTITUTIONAL GRADE DISTRIBUTION
# =========================================

st.subheader(
    "🏅 Institutional Grade Distribution"
)

grade_counts = (
    filtered_df[
        "INSTITUTIONAL_GRADE"
    ]
    .value_counts()
)

st.bar_chart(
    grade_counts
)

# =========================================
# DOWNLOADS
# =========================================

st.subheader(
    "⬇️ Export Results"
)

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Institutional Rankings CSV",
    data=csv_data,
    file_name=(
        "institutional_rankings.csv"
    ),
    mime="text/csv"
)

# =========================================
# FOOTER
# =========================================

st.markdown("---")

st.caption(
    "Enterprise Institutional Analytics Platform"
)
