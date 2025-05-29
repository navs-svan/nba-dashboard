{{ config(materialized='table') }}


SELECT
      name
    , {{ convert_minutes('minutes') }} AS minutes_converted
    , CASE {{ convert_minutes('minutes') }}
        WHEN 0 THEN 0
        ELSE 1
      END AS game_played
    , {{ create_id('team', 'date') }} AS team_date_id
    , field_goals
    , fg_attempts
    , fg_percent
    , fg_three
    , fg_three_attempts
    , fg_three_percent
    , ft_made
    , ft_attempt
    , ft_percent
    , rb_offensive
    , rb_defensive
    , rb_total
    , assists
    , steals
    , blocks
    , turnovers
    , personal_fouls
    , points
    , game_score
    , plus_minus
    , true_shoot_percent
    , efg_percent
    , fg_three_attempt_rate
    , ft_attempt_rate
    , rb_off_percent
    , rb_def_percent
    , rb_tot_percent
    , assist_percent
    , steal_percent
    , block_percent
    , turnover_percent
    , usage_percent
    , off_rating
    , def_rating
    , box_plus_minus
    , home_court
    , date
    , team
    , opponent
FROM {{ source('raw', 'raw_data')}}
