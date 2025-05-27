BEGIN; 
CREATE TABLE IF NOT EXISTS filter_order (
    filter_table TEXT PRIMARY KEY,
    order_num INTEGER
);

CREATE TABLE IF NOT EXISTS season_leader_criteria (
    team_games INTEGER,
    allnot_percent INTEGER,
    fg_percent INTEGER,
    ft_percent INTEGER,
    threep_percent INTEGER
);

CREATE TABLE IF NOT EXISTS player_images (
    image_link TEXT,
    player_name TEXT
);

CREATE TABLE IF NOT EXISTS teams (
    team TEXT NOT NULL,
    conference TEXT,
    short_name TEXT,
    logo TEXT
);
COMMIT;