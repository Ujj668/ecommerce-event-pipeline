with source as (
    select * from workspace.ecommerce_dbt.raw_events
),

cleaned as (
    select
        event_id,
        event_type,
        event_timestamp,
        user_id,
        session_id,
        product_id,
        product_name,
        category,
        cast(price as double)  as price,
        cast(quantity as int)  as quantity,
        device,
        country
    from source
    where event_id is not null
      and event_type is not null
      and user_id is not null
)

select * from cleaned