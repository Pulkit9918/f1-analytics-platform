select driver_id, given_name, family_name, nationality, date_of_birth
from {{ source('raw', 'drivers') }}