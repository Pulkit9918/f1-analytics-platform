select season, round, driver_id, stint, compound, lap_start, lap_end
from {{ source('raw', 'stints') }}