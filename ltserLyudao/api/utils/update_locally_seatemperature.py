import csv
import os
import time
from api.utils.validate import validate_datetime, validate_decimal, validate_integer
from api.models import SeaTemperatureData
from django.conf import settings
from django.db import connection

BATCH_SIZE = 1000
MAX_RETRIES = 5
RETRY_DELAY = 10


def retry_bulk_create(data_list):
    for attempt in range(MAX_RETRIES):
        try:
            SeaTemperatureData.objects.bulk_create(data_list, ignore_conflicts=True)
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(RETRY_DELAY)
    print("Max retries reached. Failed to insert records.")
    return False


try:
    table_name = SeaTemperatureData._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE;')
    print("Action: Successfully truncated table")
except Exception as e:
    print(f"ERROR: Failed to truncate table. Exception: {e}")
    exit(1)

csv_dir = os.path.join(settings.BASE_DIR, "api", "utils", "sea_temperature_csv")
if not os.path.exists(csv_dir):
    print(f"ERROR: CSV directory {csv_dir} does not exist.")
    exit(1)

csv_files = [f for f in os.listdir(csv_dir) if f.endswith(".csv")]
# csv_files = [f for f in os.listdir(csv_dir) if f == '03-202308_202404_all_sites_depositar.csv']
if not csv_files:
    print("No CSV files found in the directory.")
    exit(0)

for csv_file in csv_files:
    csv_file_path = os.path.join(csv_dir, csv_file)

    try:
        with open(csv_file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            data_list = []
            for row in reader:
                try:
                    time = validate_datetime(row.get("eventDate"), "eventDate", row)
                    seaTemperature = validate_decimal(
                        row.get("seaTemperature"), "seaTemperature", row
                    )

                    data_list.append(
                        SeaTemperatureData(
                            dataID=row.get("dataID"),
                            eventID=row.get("eventID"),
                            resourceName=row.get("resourceName"),
                            locationID=row.get("locationID"),
                            verbatimDepth=row.get("verbatimDepth"),
                            fieldNumber=row.get("fieldNumber"),
                            time=time,
                            seaTemperature=seaTemperature,
                        )
                    )
                except Exception as e:
                    print(
                        f"ERROR: Failed to process row {row} in file {csv_file}. Exception: {e}"
                    )

            try:
                # SeaTemperatureData.objects.bulk_create(data_list, ignore_conflicts=True)
                for i in range(0, len(data_list), BATCH_SIZE):
                    batch = data_list[i : i + BATCH_SIZE]
                    if not retry_bulk_create(batch):
                        print(f"Failed to process batch from file {csv_file}. Exiting.")
                        break
                print(
                    f"Inserted {len(data_list)} records from {csv_file} into SeaTemperatureData."
                )
            except Exception as e:
                print(
                    f"ERROR: Failed to insert records from {csv_file} into SeaTemperatureData. Exception: {e}"
                )
    except Exception as e:
        print(f"ERROR: Failed to read CSV file {csv_file}. Exception: {e}")
        continue
