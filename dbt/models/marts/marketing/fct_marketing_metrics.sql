{{ config(materialized='table') }}

with ad as (
    select * from {{ ref('stg_ad_performance') }}
),
campaigns as (
    select * from {{ ref('stg_campaigns') }}
),
rev as (
    select * from {{ ref('stg_customer_revenue') }}
)

select
    c.campaign_id,
    c.campaign_name,
    c.channel,
    c.start_date,
    c.end_date,
    c.budget_usd,
    
    sum(a.impressions) as total_impressions,
    sum(a.clicks) as total_clicks,
    sum(a.conversions) as total_conversions,
    sum(a.spend) as total_spend,
    
    count(distinct r.customer_id) as new_customers,
    sum(r.revenue) as total_revenue,

    -- Metrics, convert to float for calcs
    sum(a.clicks)::float / nullif(sum(a.impressions),0) as ctr,
    sum(a.conversions)::float / nullif(sum(a.clicks),0) as conversion_rate,
    sum(a.spend)::float / nullif(count(distinct r.customer_id),0) as cac,
    sum(r.revenue)::float / nullif(count(distinct r.customer_id),0) as ltv,
    sum(r.revenue)::float / nullif(sum(a.spend),0) as roas

from ad a
join campaigns c on a.campaign_id = c.campaign_id
left join rev r on a.campaign_id = r.campaign_id
group by 1,2,3,4,5,6
