from google.cloud import bigquery, storage
from datetime import datetime, timedelta
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
import os

from airflow.decorators import dag
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

import logging

logger = logging.getLogger("airflow.task")


def gcs_to_bq():
    logger.info("Appending to BigQuery Table")
    filepath = Path(__file__).resolve()

    env_file = find_dotenv(".env")
    load_dotenv(env_file)

    BUCKET = os.environ.get("GOOGLE_STORAGE_BUCKET")
    DATASET = os.environ.get("GOOGLE_BQ_RAW")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(
        filepath.parent.parent / "gcreds.json"
    )

    # Construct a BigQuery client object.
    bq_client = bigquery.Client()
    storage_client = storage.Client()

    # get uri of file
    bucket = storage_client.bucket(BUCKET)

    cur_date = datetime.now().strftime("%Y-%m-%d")

    file_name = f"export/output_{cur_date}.csv"
    blob = bucket.get_blob(file_name)
    uri = f"gs://{blob.bucket.name}/{blob.name}"

    table_id = f"{DATASET}.raw_data"

    schema = [
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("minutes", "STRING"),
        bigquery.SchemaField("field_goals", "INTEGER"),
        bigquery.SchemaField("fg_attempts", "INTEGER"),
        bigquery.SchemaField("fg_percent", "FLOAT"),
        bigquery.SchemaField("fg_three", "INTEGER"),
        bigquery.SchemaField("fg_three_attempts", "INTEGER"),
        bigquery.SchemaField("fg_three_percent", "FLOAT"),
        bigquery.SchemaField("ft_made", "INTEGER"),
        bigquery.SchemaField("ft_attempt", "INTEGER"),
        bigquery.SchemaField("ft_percent", "FLOAT"),
        bigquery.SchemaField("rb_offensive", "INTEGER"),
        bigquery.SchemaField("rb_defensive", "INTEGER"),
        bigquery.SchemaField("rb_total", "INTEGER"),
        bigquery.SchemaField("assists", "INTEGER"),
        bigquery.SchemaField("steals", "INTEGER"),
        bigquery.SchemaField("blocks", "INTEGER"),
        bigquery.SchemaField("turnovers", "INTEGER"),
        bigquery.SchemaField("personal_fouls", "INTEGER"),
        bigquery.SchemaField("points", "INTEGER"),
        bigquery.SchemaField("game_score", "FLOAT"),
        bigquery.SchemaField("plus_minus", "INTEGER"),
        bigquery.SchemaField("true_shoot_percent", "FLOAT"),
        bigquery.SchemaField("efg_percent", "FLOAT"),
        bigquery.SchemaField("fg_three_attempt_rate", "FLOAT"),
        bigquery.SchemaField("ft_attempt_rate", "FLOAT"),
        bigquery.SchemaField("rb_off_percent", "FLOAT"),
        bigquery.SchemaField("rb_def_percent", "FLOAT"),
        bigquery.SchemaField("rb_tot_percent", "FLOAT"),
        bigquery.SchemaField("assist_percent", "FLOAT"),
        bigquery.SchemaField("steal_percent", "FLOAT"),
        bigquery.SchemaField("block_percent", "FLOAT"),
        bigquery.SchemaField("turnover_percent", "FLOAT"),
        bigquery.SchemaField("usage_percent", "FLOAT"),
        bigquery.SchemaField("off_rating", "INTEGER"),
        bigquery.SchemaField("def_rating", "INTEGER"),
        bigquery.SchemaField("box_plus_minus", "FLOAT"),
        bigquery.SchemaField("home_court", "BOOLEAN"),
        bigquery.SchemaField("date", "DATE"),
        bigquery.SchemaField("team", "STRING"),
        bigquery.SchemaField("opponent", "STRING"),
    ]

    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
        schema=schema,
        write_disposition="WRITE_APPEND",
    )
    load_job = bq_client.load_table_from_uri(uri, table_id, job_config=job_config)

    load_job.result()
    logger.info("Done. Appended to raw table")


@dag(
    dag_id="bref_pipeline",
    schedule="@daily",
    start_date=datetime.now() - timedelta(days=1),
    catchup=False,
)
def Pipeline():

    web_to_gcs_task = BashOperator(
        task_id="web_to_gcs",
        bash_command="cd /opt/airflow/scraper && scrapy crawl bref_spider",
        retries=3,
    )

    gcs_to_bucket_task = PythonOperator(
        task_id="gcs_to_bucket",
        python_callable=gcs_to_bq,
        execution_timeout=timedelta(minutes=15),
        retries=3,
    )

    dbt_core_task = BashOperator(
        task_id="dbt_core",
        bash_command="cd /opt/airflow/dbt_core && dbt build",
        retries=4,
    )
    web_to_gcs_task >> gcs_to_bucket_task >> dbt_core_task


dag = Pipeline()
