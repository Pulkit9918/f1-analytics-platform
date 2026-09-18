with quali as (select * from {{ ref('stg_qualifying') }}),
     results as (select * from {{ ref('int_race_results_enriched') }})

select
    results.season,
    results.round,
    results.race_name,
    results.driver_name,
    quali.position as grid_position,
    results.position as finish_position,
    (quali.position - results.position) as positions_gained,
    results.points
from results
left join quali
    on results.season = quali.season
   and results.round = quali.round
   and results.driver_id = quali.driver_id
order by results.season, results.round, positions_gained desc