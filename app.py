import streamlit as st
import pandas as pd
import snowflake.connector
import altair as alt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Monarch Analytics Demo", layout="wide")

# --- SNOWFLAKE CONNECTION ---
creds = st.secrets["snowflake"]
conn = snowflake.connector.connect(**creds)

# Explicitly set context
conn.cursor().execute(f"USE ROLE {creds['role']}")
conn.cursor().execute(f"USE WAREHOUSE {creds['warehouse']}")
conn.cursor().execute(f"USE DATABASE {creds['database']}")
conn.cursor().execute(f"USE SCHEMA {creds['schema']}")


# --- LOAD DATA ---
@st.cache_data
def load_data():
    fct_marketing = pd.read_sql(
        "SELECT * FROM raw_mart_marketing.fct_marketing_metrics", conn
    )
    fct_ltv = pd.read_sql("SELECT * FROM raw_mart_marketing.fct_customer_ltv", conn)

    # Normalize columns to lowercase
    fct_marketing.columns = fct_marketing.columns.str.lower()
    fct_ltv.columns = fct_ltv.columns.str.lower()

    return fct_marketing, fct_ltv


fct_marketing, fct_ltv = load_data()

# --- SIDEBAR FILTERS ---
campaigns = st.sidebar.multiselect(
    "Select Campaigns", fct_marketing["campaign_name"].unique()
)

filtered_marketing = (
    fct_marketing[fct_marketing["campaign_name"].isin(campaigns)]
    if campaigns
    else fct_marketing
)

# --- KPI SUMMARY ---
st.title("Marketing Performance Dashboard")
st.write("Note: Metrics are sample data, generated for 1 year period of 2025.")
st.markdown("---")

st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("CAC", f"${filtered_marketing['cac'].mean():.2f}")
col2.metric("LTV", f"${fct_ltv['lifetime_revenue'].mean():.2f}")
col3.metric(
    "ROAS",
    f"{(filtered_marketing['total_revenue'] / filtered_marketing['total_spend']).mean():.2f}x",
)
col4.metric("Conv Rate", f"{filtered_marketing['conversion_rate'].mean()*100:.2f}%")

# --- AD PERFORMANCE METRICS PER CAMPAIGN ---
st.subheader("Ad Performance Metrics per Campaign")

# Bar chart: impressions, clicks, conversions
perf_metrics = filtered_marketing.set_index("campaign_name")[
    ["total_impressions", "total_clicks", "total_conversions"]
]
st.bar_chart(perf_metrics)

# --- CAMPAIGN-LEVEL PERFORMANCE ---
st.subheader("Campaign Spend vs. Revenue")
spend_revenue = filtered_marketing.set_index("campaign_name")[
    ["total_spend", "total_revenue"]
]
st.bar_chart(spend_revenue)

# --- CAC vs LTV ---
st.subheader("CAC vs. LTV by Campaign")
chart_data = fct_marketing.merge(fct_ltv, on="campaign_id", how="left")
st.scatter_chart(chart_data, x="cac", y="lifetime_revenue", color="campaign_name")

# --- CUSTOMER LTV DISTRIBUTION ---
st.subheader("Customer Lifetime Value Distribution")
# Use value_counts and convert to dataframe for bar_chart
ltv_counts = fct_ltv["lifetime_revenue"].round(0).value_counts().sort_index()
st.bar_chart(ltv_counts)
