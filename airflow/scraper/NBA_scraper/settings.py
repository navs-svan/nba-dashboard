

import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from datetime import datetime


filepath = Path(__file__).resolve()

dotenv_path = find_dotenv(".env")
load_dotenv(dotenv_path)


# GET POSTGRES SETTINGS (if local storage)
# DB_PASS = os.environ.get("DB_PASS")
# DB_HOST = os.environ.get("DB_HOST")
# DB_USER = os.environ.get("DB_USER")
# DB_DATA = os.environ.get("DB_DATA")
GS_BUCKET = os.environ.get("GOOGLE_STORAGE_BUCKET")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(
    filepath.parent.parent.parent / "gcreds.json"
)

BOT_NAME = "NBA_scraper"

SPIDER_MODULES = ["NBA_scraper.spiders"]
NEWSPIDER_MODULE = "NBA_scraper.spiders"



cur_date = datetime.now().strftime("%Y-%m-%d")
FEEDS = {
    f'gs://{GS_BUCKET}/export/output_{cur_date}.csv': {
        'format': 'csv',
        'overwrite': True,
        'encoding': 'utf8',
    }
}

FEED_EXPORT_FIELDS = [
    "name",
    "minutes",
    "field_goals",
    "fg_attempts",
    "fg_percent",
    "fg_three",
    "fg_three_attempts",
    "fg_three_percent",
    "ft_made",
    "ft_attempt",
    "ft_percent",
    "rb_offensive",
    "rb_defensive",
    "rb_total",
    "assists",
    "steals",
    "blocks",
    "turnovers",
    "personal_fouls",
    "points",
    "game_score",
    "plus_minus",
    "true_shoot_percent",
    "efg_percent",
    "fg_three_attempt_rate",
    "ft_attempt_rate",
    "rb_off_percent",
    "rb_def_percent",
    "rb_tot_percent",
    "assist_percent",
    "steal_percent",
    "block_percent",
    "turnover_percent",
    "usage_percent",
    "off_rating",
    "def_rating",
    "box_plus_minus",
    "home_court",
    "date",
    "team",
    "opponent",
]


# PLAYWRIGHT
"""pip install scrapy-playwright and dependencies if you want to
use the picturespider and uncomment lines 96-100"""
# DOWNLOAD_HANDLERS = {
#     "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
#     "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
# }
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"


ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 16

SPIDER_MIDDLEWARES = {
    "NBA_scraper.middlewares.DeltaFetch": 100,
}
DELTAFETCH_ENABLED = True
DELTAFETCH_RESET = False

ITEM_PIPELINES = {
    "NBA_scraper.pipelines.NbaScraperPipeline": 300,
    # "NBA_scraper.pipelines.PostgresPipeline": 400,  # if local storage
}


# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
