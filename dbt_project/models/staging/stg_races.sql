select season, round, race_name, circuit_id, race_date, race_time
from {{ source('raw', 'races') }}
where race_date is not null