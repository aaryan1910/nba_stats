select
PLAYER_NAME as player_name,
TEAM as team,
SALARY as salary,
SEASON as season,
INGESTED_AT as ingested_date
from {{ source('raw', 'RAW_PLAYER_SALARIES') }}