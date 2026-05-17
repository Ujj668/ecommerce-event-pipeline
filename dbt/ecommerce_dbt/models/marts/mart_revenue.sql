with events as (
    select * from {{ ref('stg_events') }}
),

revenue as (
    select
        event_type,
        category,
        country,
        count(*)                                              as total_events,
        count(case when event_type = 'purchase' then 1 end)  as total_purchases,
        sum(case when event_type = 'purchase'
                 then price * coalesce(quantity, 1)
                 else 0 end)                                  as total_revenue
    from events
    group by event_type, category, country
)

select * from revenue