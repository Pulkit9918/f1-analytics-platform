select season, round, driver_id, constructor_id, grid, position, points, status, fastest_lap_rank
from {{ source('raw', 'results') }}
where driver_id is not null