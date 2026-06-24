# ============================================================
# DATA ENGINEER / ANALYST BOILERPLATE REFERENCE
# Julio Cesar Zamora Ramirez — Lindavista Pipeline
# ============================================================
# How to use: Copy the section you need into your working file.
# Each block is self-contained and tested.
# ============================================================


# ------------------------------------------------------------
# 1. POSTGRESQL — SQLAlchemy connection
# ------------------------------------------------------------
from sqlalchemy import create_engine, text
import os


def get_pg_engine():
    user = os.environ["PG_USER"]
    password = os.environ["PG_PASSWORD"]
    host = os.environ.get("PG_HOST", "localhost")
    port = os.environ.get("PG_PORT", "5432")
    db = os.environ["PG_DB"]
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url)


# Usage
# engine = get_pg_engine()
# with engine.connect() as conn:
#     result = conn.execute(text("SELECT * FROM my_table LIMIT 5"))
#     df = pd.DataFrame(result.fetchall(), columns=result.keys())


# ------------------------------------------------------------
# 2. BIGQUERY — read table into DataFrame
# ------------------------------------------------------------
from google.cloud import bigquery


def bq_query(sql: str, project: str) -> "pd.DataFrame":
    client = bigquery.Client(project=project)
    return client.query(sql).to_dataframe()


# Usage
# df = bq_query("SELECT * FROM my_dataset.my_table LIMIT 100", project="my-gcp-project")


# ------------------------------------------------------------
# 3. GOOGLE CLOUD STORAGE — upload / download files
# ------------------------------------------------------------
from google.cloud import storage


def gcs_upload(local_path: str, bucket_name: str, blob_name: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_path)
    print(f"Uploaded {local_path} → gs://{bucket_name}/{blob_name}")


def gcs_download(bucket_name: str, blob_name: str, local_path: str):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(local_path)
    print(f"Downloaded gs://{bucket_name}/{blob_name} → {local_path}")


# Usage
# gcs_upload("data/output.parquet", "lindavista-bucket", "raw/output.parquet")
# gcs_download("lindavista-bucket", "raw/output.parquet", "data/output.parquet")


# ------------------------------------------------------------
# 4. REST API — GET with headers, params, error handling
# ------------------------------------------------------------
import requests


def api_get(url: str, params: dict = None, headers: dict = None) -> dict:
    headers = headers or {"Accept": "application/json"}
    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()  # raises HTTPError for 4xx/5xx
    return response.json()


# Usage
# data = api_get(
#     "https://api.example.com/v1/customers",
#     params={"page": 1, "limit": 100},
#     headers={"Authorization": f"Bearer {os.environ['API_TOKEN']}"}
# )


# ------------------------------------------------------------
# 5. REST API — POST (create / send data)
# ------------------------------------------------------------
def api_post(url: str, payload: dict, token: str) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()


# Usage
# result = api_post("https://api.example.com/orders", {"customer_id": 123}, token=os.environ["API_TOKEN"])


# ------------------------------------------------------------
# 6. DATETIME — common patterns
# ------------------------------------------------------------
from datetime import datetime, timezone, timedelta

# Always store/process in UTC
now_utc = datetime.now(timezone.utc)


# Parse a string with a known format
def parse_dt(dt_str: str, fmt: str = "%Y-%m-%d") -> datetime:
    return datetime.strptime(dt_str, fmt)


# Convert to Mexico City local time (UTC-6, no DST)
def to_cdmx(dt_utc: datetime) -> datetime:
    cdmx_offset = timezone(timedelta(hours=-6))
    return dt_utc.astimezone(cdmx_offset)


# Format for display or filenames
def dt_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


# Usage
# ts = parse_dt("2024-03-15")
# print(to_cdmx(now_utc))
# filename = f"export_{dt_slug()}.csv"


# ------------------------------------------------------------
# 7. REGEX — common patterns (describe → test → use)
# ------------------------------------------------------------
import re

# Email extraction
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# Mexican phone number (10 digits, optional +52 prefix)
PHONE_MX_RE = re.compile(r"(?:\+52)?[\s-]?\(?\d{2,3}\)?[\s-]?\d{3,4}[\s-]?\d{4}")

# Date formats: 2024-01-15 or 01/15/2024
DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4})\b")


def extract_emails(text: str) -> list:
    return EMAIL_RE.findall(text)


def clean_text(text: str) -> str:
    """Remove special characters, keep letters, numbers, spaces."""
    return re.sub(r"[^a-zA-Z0-9áéíóúÁÉÍÓÚñÑ\s]", "", text).strip()


# Usage
# emails = extract_emails("Contact: julio@example.com or info@company.mx")
# clean  = clean_text("Hello, World! ¡Hola Mundo! #$%")


# ------------------------------------------------------------
# 8. USEFUL BUILT-INS (know they exist, look up syntax)
# ------------------------------------------------------------
from collections import Counter, defaultdict
from itertools import chain, groupby
from functools import reduce

# Counter — frequency count
# words = ["apple", "banana", "apple", "cherry"]
# Counter(words)  → Counter({'apple': 2, 'banana': 1, 'cherry': 1})

# defaultdict — dict that never raises KeyError
# dd = defaultdict(list)
# dd["key"].append("value")  # works even if "key" doesn't exist

# chain — flatten a list of lists
# flat = list(chain([[1,2],[3,4],[5]]))  → [1, 2, 3, 4, 5]

# groupby — group sorted iterable (must be sorted first!)
# data = sorted([{"city":"CDMX","val":1},{"city":"CDMX","val":2},{"city":"MTY","val":3}], key=lambda x: x["city"])
# for city, group in groupby(data, key=lambda x: x["city"]):
#     print(city, list(group))

# reduce — fold a list into a single value
# total = reduce(lambda acc, x: acc + x, [1,2,3,4])  → 10


# ------------------------------------------------------------
# 9. LOGGING — production-style setup
# ------------------------------------------------------------
import logging


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(name)


# Usage
# logger = get_logger(__name__)
# logger.info("Pipeline started")
# logger.warning("Missing values detected: %d rows", 42)
# logger.error("Connection failed", exc_info=True)


# ------------------------------------------------------------
# 10. ENV VARIABLES — safe loading with python-dotenv
# ------------------------------------------------------------
from dotenv import load_dotenv

load_dotenv()  # loads .env file from project root

# Access variables
# DB_PASSWORD = os.environ["DB_PASSWORD"]       # raises KeyError if missing (safe for required vars)
# DEBUG_MODE  = os.environ.get("DEBUG", "false") # returns default if missing (safe for optional vars)


# ------------------------------------------------------------
# 11. PANDAS — common patterns worth having handy
# ------------------------------------------------------------
import pandas as pd

# Read files
# df = pd.read_csv("file.csv", parse_dates=["created_at"])
# df = pd.read_parquet("file.parquet")
# df = pd.read_json("file.json", orient="records")

# Quick inspection
# df.info()
# df.describe()
# df.isnull().sum()

# Type casting
# df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
# df["date"]   = pd.to_datetime(df["date"], format="%Y-%m-%d", utc=True)

# Write output
# df.to_csv("output.csv", index=False)
# df.to_parquet("output.parquet", index=False)


# ------------------------------------------------------------
# 12. FILE I/O — JSON and Parquet patterns
# ------------------------------------------------------------
import json


def read_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(data: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Parquet (via pandas + pyarrow)
# df.to_parquet("output.parquet", engine="pyarrow", index=False)
# df = pd.read_parquet("output.parquet")
