select season, round, driver_id, constructor_id, position, q1, q2, q3
from {{ source('raw', 'qualifying') }}