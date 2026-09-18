with results as (select * from {{ ref('int_race_results_enriched') }})

select
    season,
    constructor_name,
    count(distinct round) as races_entered,
    sum(points) as total_points,
    avg(position) as avg_finish_position,
    count(case when position = 1 then 1 end) as wins,
    count(case when position <= 3 then 1 end) as podiums
from results
group by 1, 2
order by season, total_points desc