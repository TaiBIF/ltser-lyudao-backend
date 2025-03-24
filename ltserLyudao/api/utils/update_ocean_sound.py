import requests
import re
from datetime import datetime
from api.utils.validate import validate_datetime, validate_integer
from api.models import OceanSoundIndexData
from django.db import connection

current_date = datetime.now().isoformat()
print("-" * 60)
print(f"Execution date: {current_date}")
print("Database: OceanSoundIndexData")

# Step 1: Fetch metadata from API
metadata_url = "https://data.depositar.io/api/3/action/datastore_search?resource_id=835b9da9-9b56-4a19-9667-73f81e5eb0a1"
response = requests.get(metadata_url)
resource_list = []
pattern = r"/resource/([a-zA-Z0-9\-]+)/download"

if response.status_code == 200:
    print(
        f"Successfully fetched metadata from API. Status code: {response.status_code}"
    )
    data = response.json()
    records = data.get("result", {}).get("records", [])
    for record in records:
        record_dict = {}
        resource_url = record.get("resourceID")
        location_id = record.get("locationID")
        verbatim_depth = record.get("verbatimDepth")
        if resource_url:
            match = re.search(pattern, resource_url)
            if match:
                resource_id = match.group(1)
                record_dict["resource_id"] = resource_id
                record_dict["location_id"] = location_id
                record_dict["verbatim_depth"] = verbatim_depth

                resource_list.append(record_dict)
                print(f"Action: Add resource with ID: {resource_id}")
        else:
            print(f"ERROR: There is no resource in this dataset.")
else:
    print(f"ERROR: Depositar API status code, {response.status_code}")
    exit(1)

# Step 2: Truncate table
try:
    table_name = OceanSoundIndexData._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE;')
    print("Action: Successfully truncated table")
except Exception as e:
    print(f"ERROR: Failed to truncate table. Exception: {e}")
    exit(1)

# Step 3: Start parsing resources
print("Resource Parsing Progress:")
if resource_list:
    for resource in resource_list:
        resource_id = resource.get("resource_id")
        url = f"https://data.depositar.io/zh_Hant_TW/api/3/action/datastore_search?resource_id={resource_id}"
        total_count = False
        offset = 0
        limit = 100
        records_count = 0

        print(f"- Started parsing resource: {resource_id}")
        while not total_count:
            params = {"offset": offset, "limit": limit}

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                records = data.get("result", {}).get("records", [])
                if not records:
                    print(f"ERROR: No records found for resource: {resource}")
                    break
                records_count += len(records)

                data_list = []
                for record in records:
                    time = validate_datetime(
                        record.get("measurementDeterminedDate"),
                        "measurementDeterminedDate",
                        record,
                    )

                    # 以下兩個值從 metadata_url 來
                    location_id = resource.get("location_id")
                    verbatim_depth = resource.get("verbatim_depth")

                    data_list.append(
                        OceanSoundIndexData(
                            dataID=record.get("dataID"),
                            eventID=record.get("eventID"),
                            time=time,
                            kHz0_24=record.get("0_24kHz"),
                            lower_200Hz=record.get("lower_200Hz"),
                            Hz200_1500=record.get("200_1500Hz"),
                            higher_1500Hz=record.get("higher_1500Hz"),
                            locationID=location_id,
                            verbatimDepth=verbatim_depth,
                        )
                    )

                # Batch insert into database
                try:
                    OceanSoundIndexData.objects.bulk_create(data_list)
                except Exception as e:
                    print(
                        f"ERROR: Failed to insert records for resource {resource}. Exception: {e}"
                    )
                    break

                offset += limit

                # Check if all records have been processed
                if records_count >= data.get("result", {}).get("total"):
                    print(
                        f"    - Action: Successfully inserted {records_count} records"
                    )
                    total_count = True
            else:
                print(
                    f"ERROR: Failed to fetch records for resource {resource}. Status code: {response.status_code}"
                )
                break
else:
    print("ERROR: No valid CSV resources found for parsing.")

print("All operations completed successfully.")
print("-" * 60)
