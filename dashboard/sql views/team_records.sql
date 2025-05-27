CREATE OR REPLACE VIEW team_records_view AS
WITH total_team_records AS (
	SELECT
		  team
		, SUM(fgm) AS tot_fgm
		, SUM(fga) AS tot_fga
		, SUM(ftm) AS tot_ftm
		, SUM(fta) AS tot_fta
		, SUM(fg3) AS tot_fg3
		, SUM(fg3a) AS tot_fg3a
	FROM game_results_view
	GROUP BY team
)
, avg_team_records AS (
	SELECT
		  team
		, SUM(CASE WHEN result = 'Win' THEN 1 ELSE 0 END) AS total_wins
		, SUM(CASE WHEN result = 'Loss' THEN 1 ELSE 0 END) AS total_losses
		, SUM(CASE WHEN result = 'Win' THEN 1.0 ELSE 0.0 END) / COUNT(1) AS percent_win
		, AVG(points) AS points_pg
		, AVG(fgm) AS fgm_pg
		, AVG(fga) AS fga_pg
		, AVG(ftm) AS ftm_pg
		, AVG(fta) AS fta_pg
		, AVG(fg3) AS fg3_pg
		, AVG(fg3a) AS fg3a_pg
		, AVG(oreb) AS oreb_pg
		, AVG(dreb) AS dreb_pg
		, AVG(treb) AS treb_pg
		, AVG(ast) AS ast_pg
		, AVG(stl) AS stl_pg
		, AVG(blk) AS blk_pg
		, AVG(tov) AS tov_pg
	FROM game_results_view a
	GROUP BY team
)

, team_records AS (
	SELECT
		  b.short_name
		, b.conference
		, RANK() OVER(PARTITION BY b.conference ORDER BY a.percent_win DESC) AS conference_rank
		, a.*
		, t.tot_fgm * 1.0 / t.tot_fga AS fg_percent_pg
		, t.tot_ftm * 1.0 / t.tot_fta AS ft_percent_pg
		, t.tot_fg3 * 1.0 / t.tot_fg3a as fg3_percent_pg
	FROM total_team_records t
	JOIN avg_team_records a
		ON t.team = a.team
	JOIN teams b
		on b.team = t.team
)

SELECT * FROM team_records;