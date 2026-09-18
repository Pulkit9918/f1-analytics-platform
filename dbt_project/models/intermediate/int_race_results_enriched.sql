with results as (select * from {{ ref('stg_results') }}),
     drivers as (select * from {{ ref('stg_drivers') }}),
     constructors as (select * from {{ ref('stg_constructors') }}),
     races as (select * from {{ ref('stg_races') }})

select
    results.season,
    results.round,
    races.race_name,
    races.race_date,
    results.driver_id,
    drivers.given_name || ' ' || drivers.family_name as driver_name,
    results.constructor_id,
    constructors.name as constructor_name,
    results.grid,
    results.position,
    results.points,
    results.status
from results
left join drivers on results.driver_id = drivers.driver_id
left join constructors on results.constructor_id = constructors.constructor_id
left join races on results.season = races.season and results.round = races.round