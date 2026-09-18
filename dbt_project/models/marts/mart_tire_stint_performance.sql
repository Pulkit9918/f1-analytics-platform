with laps as (select * from {{ ref('int_laps_enriched') }})

select
    season,
    round,
    driver_name,
    compound,
    stint,
    count(*) as laps_on_compound,
    avg(lap_time_sec) as avg_lap_time_sec,
    min(lap_time_sec) as best_lap_time_sec,
    max(tyre_life) as max_tyre_life
from laps
where compound is not null
group by 1,2,3,4,5
order by season, round, driver_name, stint