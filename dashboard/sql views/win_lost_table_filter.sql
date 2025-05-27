CREATE OR REPLACE VIEW win_lost_table_filter_view AS 
WITH win_lose_table_filter AS (
	SELECT
		  CONCAT(team, date) AS id
		, points AS team_score
		, opponent_score
		, opponent
		, points - opponent_score as point_diff
	FROM game_results_view
)

SELECT * FROM win_lose_table_filter;