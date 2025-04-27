

from google.cloud import bigquery, storage
from datetime import datetime, timedelta
from dotenv import find_dotenv, load_dotenv

from pathlib import Path
import sys
import os

filepath = Path(__file__).resolve()
scraper_folder = filepath.parent.parent / "scraper"
os.environ.setdefault('SCRAPY_SETTINGS_MODULE', 'NBA_scraper.settings')

sys.path.append(str(scraper_folder))
sys.path.append(str(filepath.parent.parent))

from scraper.NBA_scraper.spiders.bref_spider import BrefSpiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from airflow.decorators import dag
from airflow.operators.python import PythonOperator

def web_to_gcs():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(BrefSpiderSpider)
    process.start()


def gcs_to_bq():
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
    file_name = f"export/test_{cur_date}.csv"
    # file_name = f"export/output_{cur_date}.csv"
    blob = bucket.get_blob(file_name)
    uri = f"gs://{blob.bucket.name}/{blob.name}"

    # table_id = "your-project.your_dataset.your_table_name"
    table_id = f"{DATASET}.raw_data"

    job_config = bigquery.LoadJobConfig(
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,
        write_disposition="WRITE_APPEND",
    )
    load_job = bq_client.load_table_from_uri(
        uri, table_id, job_config=job_config
    )  # Create and API request
    load_job.result()  # Wait for the job to complete



@dag(
    dag_id="bref_pipeline",
    schedule="@daily",
    start_date=datetime.now() - timedelta(days=1),
    catchup=False,
)
def Pipeline():

    web_to_gcs_task = PythonOperator(
        task_id="web_to_gcs",
        python_callable=web_to_gcs,
        retries=3,
    )

    gcs_to_bucket_task = PythonOperator(
        task_id="gcs_to_bucket",
        python_callable=gcs_to_bq,
        retries=3,
    )

    web_to_gcs_task >> gcs_to_bucket_task


dag = Pipeline()

if __name__ == "__main__":
    web_to_gcs()
    gcs_to_bq()