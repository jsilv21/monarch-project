import streamlit as st
import pandas as pd
import snowflake.connector

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


# 2. Load data from DBT models
@st.cache_data
def load_data():
    fct_marketing = pd.read_sql(
        "SELECT * FROM raw_mart_marketing.fct_marketing_metrics", conn
    )
    fct_ltv = pd.read_sql("SELECT * FROM raw_mart_marketing.fct_customer_ltv", conn)
    return fct_marketing, fct_ltv


fct_marketing, fct_ltv = load_data()

# 3. Sidebar filters
campaigns = st.sidebar.multiselect(
    "Select Campaigns", fct_marketing["campaign_name"].unique()
)

filtered_marketing = (
    fct_marketing[fct_marketing["campaign_name"].isin(campaigns)]
    if campaigns
    else fct_marketing
)

# 4. KPI summary
st.title("Marketing Performance Dashboard")

col1, col2, col3, col4 = st.columns(4)
col1.metric("CAC", f"${filtered_marketing['cac'].mean():.2f}")
col2.metric("LTV", f"${fct_ltv['lifetime_revenue'].mean():.2f}")
col3.metric(
    "ROAS",
    f"{(filtered_marketing['revenue'] / filtered_marketing['spend']).mean():.2f}x",
)
col4.metric("Conv Rate", f"{filtered_marketing['conversion_rate'].mean()*100:.2f}%")

# 5. Charts
st.subheader("Campaign-Level Performance")

st.bar_chart(filtered_marketing.set_index("campaign_name")[["spend", "revenue"]])

st.subheader("CAC vs. LTV by Campaign")
chart_data = fct_marketing.merge(fct_ltv, on="campaign_id", how="left")
st.scatter_chart(chart_data, x="cac", y="lifetime_revenue", color="campaign_name")

# 6. Customer revenue distribution
st.subheader("Customer Lifetime Value Distribution")
st.hist_chart(fct_ltv["lifetime_revenue"])
