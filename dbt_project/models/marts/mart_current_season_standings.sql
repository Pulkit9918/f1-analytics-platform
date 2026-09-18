with results as (select * from {{ ref('int_race_results_enriched') }}),

current_season as (
    select max(season) as season from results
)

select
    r.driver_name,
    r.constructor_name,
    count(distinct r.round) as races_completed,
    sum(r.points) as total_points,
    count(case when r.position = 1 then 1 end) as wins,
    count(case when r.position <= 3 then 1 end) as podiums
from results r
join current_season cs on r.season = cs.season
group by 1, 2
order by total_points desc