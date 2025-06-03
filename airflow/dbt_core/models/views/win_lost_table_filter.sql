{{ config(materialized='view') }}

WITH win_lose_table_filter AS (
	SELECT
		  {{ create_id('team', 'date') }} AS team_date_id
		, points AS team_score
		, opponent_score
		, opponent
		, points - opponent_score as point_diff
	FROM {{ ref('game_results') }} 
)

SELECT * FROM win_lose_table_filter