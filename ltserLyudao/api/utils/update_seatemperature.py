import requests
from collections import defaultdict
from api.utils.validate import validate_datetime, validate_decimal, validate_integer
from api.models import (
    SeaTemperatureCK2023,
    SeaTemperatureDBS2023,
    SeaTemperatureGG2023,
    SeaTemperatureGW2023,
    SeaTemperatureNL2023,
    SeaTemperatureSL2023,
    SeaTemperatureWQG2023,
    SeaTemperatureYZH2023,
    SeaTemperatureZP2023,
)


SEA_TEMPERATURE_TABLES = [
    SeaTemperatureCK2023,
    SeaTemperatureDBS2023,
    SeaTemperatureGG2023,
    SeaTemperatureGW2023,
    SeaTemperatureNL2023,
    SeaTemperatureSL2023,
    SeaTemperatureWQG2023,
    SeaTemperatureYZH2023,
    SeaTemperatureZP2023,
]

LOCATIONID_MAP = {
    "CK": SeaTemperatureCK2023,
    "DBS": SeaTemperatureDBS2023,
    "GG": SeaTemperatureGG2023,
    "GW": SeaTemperatureGW2023,
    "NL": SeaTemperatureNL2023,
    "SL": SeaTemperatureSL2023,
    "WQG": SeaTemperatureWQG2023,
    "YZH": SeaTemperatureYZH2023,
    "ZP": SeaTemperatureZP2023,
}

# Step 1: Fetch metadata from API
metadata_url = (
    "https://data.depositar.io/api/3/action/package_show?id=ltser-lyudao-seatemperature"
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

# # Step 2: Truncate all tables
# for table in SEA_TEMPERATURE_TABLES:
#     try:
#         table.objects.all().delete()
#         print(f'Action: Successfully truncated table {table.__name__}')
#     except Exception as e:
#         print(f'ERROR: Failed to truncate table {table.__name__}. Exception: {e}')
#         exit(1)

# Step 3: Process each resource
for resource in resource_list:
    url = f"https://data.depositar.io/zh_Hant_TW/api/3/action/datastore_search?resource_id={resource}"
    offset = 0
    limit = 100
    total_count = False
    grouped_data = defaultdict(list)  # Group data by locationID

    print(f"- Started parsing resource: {resource}")
    while not total_count:
        params = {"offset": offset, "limit": limit}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(
                f"ERROR: Failed to fetch records for resource {resource}. Status code: {response.status_code}"
            )
            break

        data = response.json()
        records = data.get("result", {}).get("records", [])
        if not records:
            print(f"ERROR: No records found for resource: {resource}")
            break

        for record in records:
            locationID = record.get("locationID")
            if locationID in LOCATIONID_MAP:
                grouped_data[locationID].append(record)
            else:
                print(f"WARNING: Skipping record with unknown locationID {locationID}.")

        offset += limit
        # if offset >= data.get('result', {}).get('total', 0):
        if offset > 1000:
            total_count = True

    # Insert grouped data into respective tables
    for locationID, rows in grouped_data.items():
        table = LOCATIONID_MAP[locationID]
        data_list = []
        existing_ids = set(table.objects.values_list("dataID", flat=True))

        for row in rows:
            dataID = row.get("dataID")
            if dataID in existing_ids:
                print(f"Skipping duplicate record with dataID={dataID}")
                continue

            try:
                time = validate_datetime(row.get("eventDate"), "eventDate", row)
                seaTemperature = validate_decimal(
                    row.get("seaTemperature"), "seaTemperature", row
                )

                data_list.append(
                    table(
                        dataID=dataID,
                        eventID=row.get("eventID"),
                        resourceName=row.get("resourceName"),
                        locationID=locationID,
                        verbatimDepth=row.get("verbatimDepth"),
                        fieldNumber=row.get("fieldNumber"),
                        time=time,
                        seaTemperature=seaTemperature,
                    )
                )
            except Exception as e:
                print(f"ERROR: Validation failed for record {row}. Exception: {e}")

        try:
            table.objects.bulk_create(data_list, ignore_conflicts=True)
            print(f"Inserted {len(data_list)} records into {table.__name__}.")
        except Exception as e:
            print(
                f"ERROR: Failed to insert records into {table.__name__}. Exception: {e}"
            )
