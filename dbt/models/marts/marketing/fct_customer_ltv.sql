{{ config(materialized='table') }}

-- Note - 1 row per customer here, but in normal scenario would have multiple rows for monthly payments, renewals, etc.
-- in those cases would have to handle churn differently

select
    customer_id,
    campaign_id,
    plan,
    revenue as lifetime_revenue,
    months_active,
    churned
from {{ ref('stg_customer_revenue') }}
