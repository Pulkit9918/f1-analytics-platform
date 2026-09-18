with laps as (select * from {{ ref('stg_laps') }}),
     stints as (select * from {{ ref('stg_stints') }}),
     drivers as (select * from {{ ref('stg_drivers') }})

select
    laps.season,
    laps.round,
    laps.driver_id,
    drivers.given_name || ' ' || drivers.family_name as driver_name,
    laps.lap_number,
    laps.lap_time_sec,
    laps.position,
    laps.compound,
    laps.tyre_life,
    stints.stint
from laps
left join drivers on laps.driver_id = drivers.driver_id
left join stints
    on laps.season = stints.season
   and laps.round = stints.round
   and laps.driver_id = stints.driver_id
   and laps.lap_number between stints.lap_start and stints.lap_end