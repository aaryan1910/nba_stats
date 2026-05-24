select
PLAYER_NAME as player_name,
TEAM as team,
G as games_played,
PER as player_efficiency_rating,    
"TS%" as true_shooting_percentage,
"USG%" as usage_percentage,
OWS as offensive_win_shares,
DWS as defensive_win_shares,
WS as win_shares,
OBPM as offensive_box_plus_minus,
DBPM as defensive_box_plus_minus,
BPM as box_plus_minus,
VORP as value_over_replacement_player,
SEASON as season,
INGESTED_AT as ingested_at

from {{ source('raw', 'RAW_ADVANCED_STATS') }}
where (TEAM = 'TOT'
or PLAYER_NAME not in (
    select PLAYER_NAME 
    from {{ source('raw', 'RAW_ADVANCED_STATS') }} 
    where TEAM = 'TOT'
))
and G > 0