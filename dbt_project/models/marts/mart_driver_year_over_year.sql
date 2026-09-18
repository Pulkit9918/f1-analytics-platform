with results as (select * from {{ ref('int_race_results_enriched') }})

select
    season,
    driver_name,
    count(distinct constructor_name) as teams_raced_for,
    count(distinct round) as races_entered,
    sum(points) as total_points,
    avg(grid) as avg_grid_position,
    avg(position) as avg_finish_position,
    avg(grid - position) as avg_positions_gained,
    count(case when position = 1 then 1 end) as wins
from results
group by 1, 2
order by driver_name, season