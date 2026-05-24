select
    PLAYER_ID as player_id,
    PLAYER_NAME as player_name,
    TEAM_ABBREVIATION as team,
    GP as games_played,
    "MIN" as minutes_per_game,
    PTS as points,
    AST as assists,
    REB as rebounds,
    STL as steals,
    BLK as blocks,
    FG_PCT as fg_percentage,
    FG3_PCT as fg3_percentage,
    FT_PCT as ft_percentage,
    TOV as turnovers,
    PLUS_MINUS as plus_minus,
    SEASON as season,
    INGESTED_AT as ingested_at

from {{ source('raw', 'RAW_PLAYER_STATS') }}
where GP > 0