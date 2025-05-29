{{ config(materialized='view') }}

WITH off_def_rating AS (
	SELECT
		  name
		, AVG(off_rating) AS off_rating
		, AVG(def_rating) AS def_rating
		, team
	FROM {{ ref('props') }}
	GROUP BY name, team
)

SELECT * FROM off_def_rating