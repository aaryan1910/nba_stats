select
    distinct advanced.player_name,
    advanced.team,
    advanced.player_efficiency_rating,
    advanced.win_shares,
    advanced.box_plus_minus,
    advanced.value_over_replacement_player,
    salaries.salary,
    player.games_played,
    player.minutes_per_game,
    player.points,
    player.rebounds,
    player.assists,
    player.steals,
    player.blocks,
    player.fg_percentage,
    player.fg3_percentage,
    player.ft_percentage,
    player.turnovers,
    player.plus_minus,
    advanced.true_shooting_percentage,
    advanced.usage_percentage,
    advanced.offensive_win_shares,
    advanced.defensive_win_shares,
    advanced.offensive_box_plus_minus,
    advanced.defensive_box_plus_minus,

round(
    (advanced.player_efficiency_rating * 0.4 + 
     advanced.value_over_replacement_player * 0.3 + 
     advanced.win_shares * 0.3) 
    / nullif(salaries.salary / 1000000, 0),
4) as value_index

from {{ ref('stg_advanced_stats') }} as advanced 
JOIN {{ ref('stg_player_salaries') }} as salaries ON 
advanced.player_name = salaries.player_name
AND advanced.team = salaries.team
join {{ ref('stg_player_stats') }} as player
    on advanced.player_name = player.player_name
    and advanced.team = player.team

where player.games_played >= 30
and salaries.salary >= 1000000