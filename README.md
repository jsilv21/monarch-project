# Monarch Analytics Project

## Purpose

This Project delivers sample marketing analytics by generating synthetic data and showcasing a complete data pipeline. It provides insights into key metrics such as customer acquisition cost (CAC), lifetime value (LTV), and return on ad spend (ROAS).

## Architecture

The project demonstrates a modern data stack:

1. **Sample CSVs**: Synthetic data is generated and stored as CSV files.
2. **S3**: CSVs are uploaded to an S3 bucket for centralized storage.
3. **Snowflake**: Data is ingested into Snowflake for efficient querying and analysis.
4. **DBT**: DBT transforms raw data into analytics-ready datasets.
5. **Streamlit**: An interactive dashboard visualizes marketing metrics.

## Data Pipeline

1. **Data Generation**: Synthetic data includes:

   - `dim_campaigns`: Campaign metadata.
   - `dim_date`: Date dimension for time-based analysis.
   - `fact_ad_performance`: Daily ad performance metrics.
   - `fact_customer_revenue`: Customer revenue data.

2. **Data Storage**: Generated CSVs are uploaded to S3.
3. **Data Warehousing**: Data is loaded into Snowflake for analysis.
4. **Data Transformation**: DBT ensures data is clean and analytics-ready.
5. **Dashboard**: A Streamlit app visualizes marketing performance.

```mermaid
flowchart TD
    subgraph SOURCES
        A1["Campaign Data
        (CSV)"]
        A2["Date Data
        (CSV)"]
    end
    subgraph INGESTION
        B1["S3 Bucket"]
        B2["Snowflake Integration"]
    end
    subgraph WAREHOUSE
        C1["Snowflake Raw Schema"]
        C2["Snowflake Staging, Mart Schema"]
    end
    subgraph DBT_TRANSFORM
        T1["dbt Models & Transforms"]
    end
    subgraph BI_LAYER
        D1["Streamlit (Or other apps)"]
        D2["Marketing Metrics Dashboard"]
    end
    %% Data Flow
    A1 --> B1
    A2 --> B1
    B1 --> B2
    B2 --> C1
    C1 --> T1
    T1 --> C2
    C2 --> D1
    D1 --> D2

    %% Circular reference for dbt
    C2 --> T1
```

![Snowflake](/images/snowflake.png)
