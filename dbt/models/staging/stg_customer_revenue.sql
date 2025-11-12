{{ config(materialized='view') }}

select
    customer_id,
    campaign_id,
    cast(date_acquired as date) as date_acquired,
    plan,
    revenue_usd as revenue,
    months_active,
    churned
from {{ source('raw', 'fact_customer_revenue') }}
