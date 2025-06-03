{{ config(materialized='view') }}

WITH individual_result AS (
	SELECT 
		  team
		, date
		, SUM(points) AS points
		, SUM(field_goals) AS fgm
		, SUM(fg_attempts) AS fga
		, SUM(field_goals) * 1.0 / NULLIF(SUM(fg_attempts), 0) AS fg_percent
		, SUM(fg_three) AS fg3
		, SUM(fg_three_attempts) AS fg3a
		, SUM(fg_three) * 1.0 / NULLIF(SUM(fg_three_attempts), 0) AS fg3_percent
		, SUM(ft_made) AS ftm
		, SUM(ft_attempt) AS fta
		, SUM(ft_made) * 1.0 / NULLIF(SUM(ft_attempt), 0) AS ft_percent
		, SUM(rb_offensive) AS oreb
		, SUM(rb_defensive) AS dreb
		, SUM(rb_total) AS treb
		, SUM(assists) AS ast
		, SUM(steals) AS stl
		, SUM(blocks) AS blk
		, SUM(turnovers) AS tov
		, SUM(personal_fouls) AS pf
		, MIN(CAST(home_court AS INT64)) AS home_court
		, opponent
	FROM {{ ref('props')}}
	GROUP BY team, date, opponent
)

, game_result AS (
	SELECT
		  a.date
		, a.team
		, a.opponent
		, a.points
		, a.fgm
		, a.fga
		, a.fg_percent
		, a.fg3
		, a.fg3a
		, a.fg3_percent
		, a.ftm
		, a.fta
		, a.ft_percent
		, a.oreb
		, a.dreb
		, a.treb
		, a.ast
		, a.stl
		, a.blk
		, a.tov
		, a.pf
		, b.points AS opponent_score
		, CASE 
			WHEN a.points > b.points THEN 'Win'
			ELSE 'Loss'
		  END AS result
		, CASE
			WHEN a.home_court = 1 THEN 'Home'
			ELSE 'Away'
		  END AS home_court
	FROM individual_result a
	JOIN individual_result b
		ON a.opponent = b.team
		AND a.date = b.date
)

SELECT * FROM game_result