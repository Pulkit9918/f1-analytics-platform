with pit_stops as (select * from {{ ref('stg_pit_stops') }}),
     results as (select * from {{ ref('int_race_results_enriched') }})

select
    results.season,
    results.round,
    results.race_name,
    results.constructor_name,
    results.driver_name,
    count(pit_stops.stop) as total_stops,
    avg(pit_stops.duration_ms) as avg_stop_duration_ms,
    min(pit_stops.duration_ms) as fastest_stop_ms,
    results.position as final_position
from pit_stops
left join results
    on pit_stops.season = results.season
   and pit_stops.round = results.round
   and pit_stops.driver_id = results.driver_id
group by 1,2,3,4,5,results.position