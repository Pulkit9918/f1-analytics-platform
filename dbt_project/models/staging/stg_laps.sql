select season, round, driver_id, lap_number, lap_time_sec, position, compound, tyre_life
from {{ source('raw', 'laps') }}
where lap_time_sec is not null