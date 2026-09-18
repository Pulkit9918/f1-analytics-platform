with results as (select * from {{ ref('int_race_results_enriched') }})

select
    season,
    round,
    race_date,
    driver_name,
    constructor_name,
    points,
    sum(points) over (
        partition by season, driver_name
        order by round
        rows between unbounded preceding and current row
    ) as cumulative_points
from results
order by season, driver_name, round