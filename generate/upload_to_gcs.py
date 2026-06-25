import os
from google.cloud import storage

# with this google.cloud i am speaking directly to my cloud account
# -- Configuration --------------
BUCKET_NAME = "lindavista-raw-data-jcz"
LOCAL_DIR = "data/raw"


def upload_to_gcs():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    for filename in os.listdir(LOCAL_DIR):
        if filename.endswith(".csv"):
            local_path = os.path.join(LOCAL_DIR, filename)
            blob = bucket.blob(f"raw/{filename}")
            blob.upload_from_filename(local_path)
            print(f"✅ Uploaded: {filename}")


if __name__ == "__main__":
    upload_to_gcs()
