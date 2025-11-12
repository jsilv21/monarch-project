{{ config(materialized='view') }}

select
    campaign_id,
    name as campaign_name,
    channel,
    start_date,
    end_date,
    budget_usd,
    owner
from {{ source('raw', 'dim_campaigns') }}
