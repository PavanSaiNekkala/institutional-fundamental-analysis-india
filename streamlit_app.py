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

    "data/exports/sector_rotation.csv",

    "data/exports/factor_scores.csv",

    "data/exports/model_portfolio.csv",

    "data/exports/ai_research_reports.csv"
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
python collectors/nse_collector.py
python collectors/screener_collector.py
python preprocessing/cleaner.py
python scoring/growth_score.py
python scoring/quality_score.py
python scoring/ownership_score.py
python scoring/valuation_score.py
python scoring/factor_model.py
python scoring/final_ranker.py
python analytics/compounder_detector.py
python analytics/institutional_buying.py
python analytics/sector_rotation.py
python analytics/portfolio_builder.py
python analytics/risk_engine.py
python analytics/ai_research_assistant.py
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

    factor_scores = pd.read_csv(
        "data/exports/factor_scores.csv"
    )

    portfolio = pd.read_csv(
        "data/exports/model_portfolio.csv"
    )

    ai_reports = pd.read_csv(
        "data/exports/ai_research_reports.csv"
    )

    return (

        rankings,

        compounders,

        institutional,

        sectors,

        factor_scores,

        portfolio,

        ai_reports
    )


(
    rankings,

    compounders,

    institutional,

    sectors,

    factor_scores,

    portfolio,

    ai_reports

) = load_data()


# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.title("Institutional Filters")

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

selected_market_cap = st.sidebar.selectbox(
    "Market Cap",
    ["ALL"] + sorted(
        rankings[
            "MARKET_CAP_CATEGORY"
        ].dropna().unique().tolist()
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

if selected_market_cap != "ALL":

    filtered_rankings = filtered_rankings[
        filtered_rankings[
            "MARKET_CAP_CATEGORY"
        ] == selected_market_cap
    ]


# =====================================================
# HEADER
# =====================================================

st.title(
    "🇮🇳 Institutional Fundamental Analysis Platform"
)

st.markdown(
    """
Professional Indian Equity Institutional Analytics System
"""
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
    round(
        filtered_rankings[
            "FINAL_SCORE"
        ].mean(),
        2
    )
)

col3.metric(
    "Top Sector",
    sectors.iloc[0]["SECTOR"]
)

col4.metric(
    "Top Rating",
    filtered_rankings["RATING"].mode()[0]
)


# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([

    "🏆 Rankings",

    "💎 Compounders",

    "🏦 Institutional Buying",

    "📊 Sector Analytics",

    "🔥 Heatmaps",

    "📁 Portfolio",

    "🤖 AI Research"
])


# =====================================================
# TAB 1 — RANKINGS
# =====================================================

with tab1:

    st.subheader(
        "Institutional Rankings"
    )

    ranking_columns = [

        "FINAL_RANK",

        "SYMBOL",

        "SECTOR",

        "MARKET_CAP_CATEGORY",

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
        filtered_rankings[
            available_columns
        ],
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

    st.subheader(
        "Long-Term Compounders"
    )

    compounder_columns = [

        "COMPOUNDER_RANK",

        "SYMBOL",

        "SECTOR",

        "MARKET_CAP_CATEGORY",

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

    st.subheader(
        "Institutional Accumulation"
    )

    institutional_columns = [

        "INSTITUTIONAL_RANK",

        "SYMBOL",

        "SECTOR",

        "MARKET_CAP_CATEGORY",

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

    st.subheader(
        "Sector Rotation Analysis"
    )

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
# TAB 5 — HEATMAPS
# =====================================================

with tab5:

    st.subheader(
        "Institutional Sector Heatmap"
    )

    sector_heatmap = factor_scores.groupby(
        "SECTOR"
    ).agg({

        "FACTOR_SCORE": "mean",

        "FINAL_SCORE": "mean",

        "SYMBOL": "count"

    }).reset_index()

    sector_heatmap.rename(columns={

        "SYMBOL": "TOTAL_STOCKS"

    }, inplace=True)

    fig5 = px.treemap(

        sector_heatmap,

        path=["SECTOR"],

        values="TOTAL_STOCKS",

        color="FACTOR_SCORE",

        hover_data=[

            "FINAL_SCORE",

            "TOTAL_STOCKS"
        ],

        title="Sector Leadership Heatmap"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )


    # =====================================
    # MARKET CAP DISTRIBUTION
    # =====================================

    st.subheader(
        "Market Cap Distribution"
    )

    market_cap_data = factor_scores[
        "MARKET_CAP_CATEGORY"
    ].value_counts().reset_index()

    market_cap_data.columns = [

        "MARKET_CAP_CATEGORY",

        "COUNT"
    ]

    fig6 = px.pie(

        market_cap_data,

        names="MARKET_CAP_CATEGORY",

        values="COUNT",

        title="Market Cap Segmentation"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )


    # =====================================
    # FACTOR DISTRIBUTION
    # =====================================

    st.subheader(
        "Institutional Factor Distribution"
    )

    fig7 = px.histogram(

        factor_scores,

        x="FACTOR_SCORE",

        nbins=30,

        color="FACTOR_GRADE",

        title="Factor Score Distribution"
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )


    # =====================================
    # TOP FACTOR STOCKS
    # =====================================

    st.subheader(
        "Elite Institutional Stocks"
    )

    elite_stocks = factor_scores.sort_values(
        by="FACTOR_SCORE",
        ascending=False
    ).head(20)

    elite_columns = [

        "FACTOR_RANK",

        "SYMBOL",

        "SECTOR",

        "MARKET_CAP_CATEGORY",

        "FACTOR_SCORE",

        "FACTOR_GRADE",

        "FINAL_SCORE"
    ]

    st.dataframe(
        elite_stocks[elite_columns],
        use_container_width=True
    )


# =====================================================
# TAB 6 — PORTFOLIO
# =====================================================

with tab6:

    st.subheader(
        "Institutional Model Portfolio"
    )

    portfolio_columns = [

        "PORTFOLIO_RANK",

        "SYMBOL",

        "SECTOR",

        "MARKET_CAP_CATEGORY",

        "FACTOR_SCORE",

        "PORTFOLIO_WEIGHT"
    ]

    available_portfolio_columns = [
        col for col in portfolio_columns
        if col in portfolio.columns
    ]

    st.dataframe(
        portfolio[
            available_portfolio_columns
        ],
        use_container_width=True
    )


    # =====================================
    # SECTOR ALLOCATION
    # =====================================

    st.subheader(
        "Portfolio Sector Allocation"
    )

    sector_alloc = portfolio[
        "SECTOR"
    ].value_counts().reset_index()

    sector_alloc.columns = [

        "SECTOR",

        "COUNT"
    ]

    fig9 = px.pie(

        sector_alloc,

        names="SECTOR",

        values="COUNT",

        title="Sector Allocation"
    )

    st.plotly_chart(
        fig9,
        use_container_width=True
    )


    # =====================================
    # MARKET CAP ALLOCATION
    # =====================================

    st.subheader(
        "Portfolio Market Cap Allocation"
    )

    cap_alloc = portfolio[
        "MARKET_CAP_CATEGORY"
    ].value_counts().reset_index()

    cap_alloc.columns = [

        "MARKET_CAP_CATEGORY",

        "COUNT"
    ]

    fig10 = px.bar(

        cap_alloc,

        x="MARKET_CAP_CATEGORY",

        y="COUNT",

        color="MARKET_CAP_CATEGORY",

        title="Market Cap Allocation"
    )

    st.plotly_chart(
        fig10,
        use_container_width=True
    )


    # =====================================
    # TOP PORTFOLIO STOCKS
    # =====================================

    st.subheader(
        "Top Portfolio Holdings"
    )

    fig11 = px.bar(

        portfolio.head(10),

        x="SYMBOL",

        y="FACTOR_SCORE",

        color="SECTOR",

        title="Top Portfolio Holdings"
    )

    st.plotly_chart(
        fig11,
        use_container_width=True
    )


# =====================================================
# TAB 7 — AI RESEARCH
# =====================================================

with tab7:

    st.subheader(
        "AI Institutional Research Assistant"
    )

    selected_stock = st.selectbox(

        "Select Stock",

        sorted(
            ai_reports["SYMBOL"].unique()
        )
    )

    stock_data = ai_reports[
        ai_reports["SYMBOL"] == selected_stock
    ]

    if not stock_data.empty:

        row = stock_data.iloc[0]

        st.markdown(
            f"## {selected_stock}"
        )

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric(
            "Institutional Rating",
            row["RATING"]
        )

        metric2.metric(
            "Factor Score",
            round(
                row["FACTOR_SCORE"],
                2
            )
        )

        metric3.metric(
            "Final Score",
            round(
                row["FINAL_SCORE"],
                2
            )
        )

        st.markdown(
            "### AI Research Summary"
        )

        st.write(
            row["AI_RESEARCH_SUMMARY"]
        )


# =====================================================
# SCORE DISTRIBUTION
# =====================================================

st.subheader(
    "📈 Institutional Score Distribution"
)

fig12 = px.histogram(
    filtered_rankings,
    x="FINAL_SCORE",
    nbins=20,
    title="Final Institutional Score Distribution"
)

st.plotly_chart(
    fig12,
    use_container_width=True
)


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "Institutional Fundamental Analysis Platform | India"
)
