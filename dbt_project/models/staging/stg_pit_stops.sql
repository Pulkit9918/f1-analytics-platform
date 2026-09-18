select season, round, driver_id, stop, lap, pit_time, duration_ms
from {{ source('raw', 'pit_stops') }}
where duration_ms is not null