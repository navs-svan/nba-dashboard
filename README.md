
# NBA 2024-25 Season Dashboard

This project automates the scraping of NBA 2024–25 season box scores from [Basketball Reference](https://www.basketball-reference.com/leagues/NBA_2025_games.html) and stores the raw data in a Google Cloud Storage bucket. The data is then transformed using dbt Core and loaded into Google BigQuery. From there, it is connected to Power BI to build interactive reports and dashboards.

The entire workflow is orchestrated using Apache Airflow, containerized with Docker, and deployed on Google Cloud Platform resources provisioned via Terraform.

### Requirements

* Docker
* Terraform
* Power BI
* GCP Account

### Usage

1. Fill in the variables and rename accordingly:
    
    * [var.tf.example](./terraform/var.tf.example) 
    * [dev.env](./airflow/dev.env)
    * [gcreds.json.example](./airflow/gcred.json.example) (Not Recommended if project is shared with others)
2. Run terraform commands inside of the [terraform](./terraform/) directory. These steps create the GCS and Bigquery infrastructure.
    * `terraform init`
    * `terraform apply`
3. Run docker commands inside of the [airflow](./airflow/) directory. These steps set up the airflow orchestration inside docker.
    
    * `docker compose build`
    * `docker compose up airflow-init`
    * `docker compose up -d`
4. Trigger the DAG

### Visualization

A PowerBI report can be interacted with through this [link](https://app.powerbi.com/view?r=eyJrIjoiYjc0NTQ1ZGQtYzUzZC00ZGUxLThjMjMtYzI2NmJjZDkyZGZhIiwidCI6ImJkMDNhNzM1LTJhYTMtNGNjYS05NzIyLTJhZTQ5MjlhYjNlYyIsImMiOjEwfQ%3D%3D). Several measures were created using complex DAX queries to create some of the more interesting visuals. Snapshots of the dashboard can be seen below.

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
