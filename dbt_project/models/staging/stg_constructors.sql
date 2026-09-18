select constructor_id, name, nationality
from {{ source('raw', 'constructors') }}