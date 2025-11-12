{{ config(materialized='table') }}

with ad_agg as (
    select
        campaign_id,
        sum(impressions) as total_impressions,
        sum(clicks) as total_clicks,
        sum(conversions) as total_conversions,
        sum(spend) as total_spend
    from {{ ref('stg_ad_performance') }}
    group by campaign_id
),

rev_agg as (
    select
        campaign_id,
        count(distinct customer_id) as new_customers,
        sum(revenue) as total_revenue
    from {{ ref('stg_customer_revenue') }}
    group by campaign_id
)

select
    c.campaign_id,
    c.campaign_name,
    c.channel,
    c.start_date,
    c.end_date,
    c.budget_usd,
    
    a.total_impressions,
    a.total_clicks,
    a.total_conversions,
    a.total_spend,
    
    r.new_customers,
    r.total_revenue,
    
    -- Metrics
    a.total_clicks::float / nullif(a.total_impressions,0) as ctr,
    a.total_conversions::float / nullif(a.total_clicks,0) as conversion_rate,
    a.total_spend::float / nullif(r.new_customers,0) as cac,
    r.total_revenue::float / nullif(r.new_customers,0) as ltv,
    r.total_revenue::float / nullif(a.total_spend,0) as roas

from {{ ref('stg_campaigns') }} c
left join ad_agg a on c.campaign_id = a.campaign_id
left join rev_agg r on c.campaign_id = r.campaign_id
