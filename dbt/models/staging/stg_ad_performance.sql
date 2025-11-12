{{ config(materialized='view') }}

select
    campaign_id,
    cast(date as date) as date,
    impressions,
    clicks,
    conversions,
    ROUND(spend_usd,2) as spend
from {{ source('raw', 'fact_ad_performance') }}
