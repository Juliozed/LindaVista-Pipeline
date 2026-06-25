import os
from google.cloud import bigquery

# ── CONFIGURATION ─────────────────────────────────────
PROJECT_ID = "lindavista-pipeline"
DATASET_ID = "raw"
BUCKET_NAME = "lindavista-raw-data-jcz"

TABLES = [
    "employees",
    "services",
    "clients",
    "special_instructions",
    "bookings",
]


def load_to_bigquery():
    client = bigquery.Client()

    for table in TABLES:
        uri = f"gs://{BUCKET_NAME}/raw/{table}.csv"

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,  # skip header row
            autodetect=True,  # auto-detect column types
            write_disposition="WRITE_TRUNCATE",  # replace if exists
        )

        table_ref = f"{PROJECT_ID}.{DATASET_ID}.{table}"

        print(f"Loading {table}...")
        job = client.load_table_from_uri(uri, table_ref, job_config=job_config)
        job.result()  # wait for job to complete

        table_obj = client.get_table(table_ref)
        print(f"✅ {table}: {table_obj.num_rows} rows loaded")


if __name__ == "__main__":
    load_to_bigquery()
