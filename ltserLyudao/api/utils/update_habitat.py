import requests
from api.utils.validate import validate_date, validate_integer
from api.models import HabitatData
from django.db import connection

# Step 1: Fetch metadata from API
metadata_url = (
    "https://data.depositar.io/api/3/action/package_show?id=ltser-lyudao-habitat"
)
response = requests.get(metadata_url)
resource_list = []

if response.status_code == 200:
    print(
        f"Successfully fetched metadata from API. Status code: {response.status_code}"
    )
    data = response.json()
    records = data.get("result", {}).get("resources", [])
    for record in records:
        file_format = record.get("format")
        resource_id = record.get("id")
        if file_format == "CSV":
            resource_list.append(resource_id)
            print(
                f"Action: Add resource with ID: {resource_id} and format: {file_format}"
            )
        else:
            print(f"ERROR: Resource with ID: {resource_id} is not in CSV format.")
else:
    print(f"ERROR: Depositar API status code, {response.status_code}")
    exit(1)

# Step 2: Truncate table
try:
    table_name = HabitatData._meta.db_table
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
        url = f"https://data.depositar.io/zh_Hant_TW/api/3/action/datastore_search?resource_id={resource}"
        total_count = False
        offset = 0
        limit = 100
        records_count = 0

        print(f"- Started parsing resource: {resource}")
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
                    # Data validation and extraction
                    time = validate_date(record.get("eventDate"), "eventDate", record)
                    Score = validate_integer(record.get("Score"), "Score", record)

                    data_list.append(
                        HabitatData(
                            dataID=record.get("dataID"),
                            eventID=record.get("eventID"),
                            time=time,
                            season=record.get("Season"),
                            river=record.get("river"),
                            locationID=record.get("locationID"),
                            factor=record.get("Factor"),
                            score=Score,
                            samplingProtocol=record.get("samplingProtocol"),
                        )
                    )

                # Batch insert into database
                try:
                    HabitatData.objects.bulk_create(data_list)
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
