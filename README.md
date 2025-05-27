
# NBA 2024-25 Season Dashboard

This project scrapes [NBA 2024-25 Season boxscores](https://www.basketball-reference.com/leagues/NBA_2025_games.html) from Basketball Reference and stores it into a local Postgres database. The scraping script and postgres database is containerized using Docker.

### Usage

1. Set up Docker Desktop 

2. Run the command `mv dev.env .env` and fill in the necessary variables

3. Build the containers using the command `docker compose build`

4. Run the containers using the command `docker compose up -d`
    * Each time the containers start, the script scrapes boxscore data from Basketball Reference

5. To have the latest data, run the command `docker compose start` or start the containers through the Docker Desktop application 

### Visualization

A PowerBI dashboard was created which can be interacted with through this [link](https://app.powerbi.com/view?r=eyJrIjoiYjc0NTQ1ZGQtYzUzZC00ZGUxLThjMjMtYzI2NmJjZDkyZGZhIiwidCI6ImJkMDNhNzM1LTJhYTMtNGNjYS05NzIyLTJhZTQ5MjlhYjNlYyIsImMiOjEwfQ%3D%3D). Several measures were created using complex DAX queries to create some of the more interesting visuals. Snapshots of the dashboard can be seen below.

##### Team Stats Overview Page 

![Page1-team_stats_overview](/imgs/team_stats_overview.png)
   
#### Team Raw Stats Page

![Page2-team_raw_stats](/imgs/team_raw_stats.png)

#### Team Specific Stats Page

![Page3-team_specific_stats](/imgs/team_specific_stats.png)

#### Player Stats Overview Page

![Page4-player_stats_overview](/imgs/player_stats_overview.png)

#### Player Raw Stats Page

![Page5-player_raw_stats](/imgs/player_raw_stats.png)

#### Player Specific Stats Page

![Page6-player_specific_stats](/imgs/player_specific_stats.png)

#### Player History Stats Page

![Page7-player_history_stats](/imgs/player_history_stats.png)

#### Scatter Plot Correlation Page

![Page8-scatter_plot](/imgs/scatter_plot.png)
