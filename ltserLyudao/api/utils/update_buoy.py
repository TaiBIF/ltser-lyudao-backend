import requests
from api.utils.validate import validate_date, combine_datetime
from api.models import BuoyData
from django.db import connection

# Step 1: Fetch metadata from API
metadata_url = (
    "https://data.depositar.io/api/3/action/package_show?id=ltser-lyudao-buoy"
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
    table_name = BuoyData._meta.db_table
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
                    date = validate_date(record.get("eventDate"), "eventDate", record)
                    combined_datetime = combine_datetime(
                        record.get("eventDate"), record.get("eventTime"), record
                    )

                    data_list.append(
                        BuoyData(
                            dataID=record.get("dataID"),
                            eventID=record.get("eventID"),
                            eventDate=date,
                            eventTime=record.get("eventTime"),
                            locationID=record.get("locationID"),
                            underwater_par=record.get("Underwater PAR"),
                            terrestrial_par=record.get("Terrestrial PAR"),
                            exo_temperature=record.get("EXO Temperature"),
                            sp_cond=record.get("Sp Cond"),
                            salinity=record.get("Salinity"),
                            ph=record.get("pH"),
                            odo_sat=record.get("ODOSat"),
                            odo=record.get("ODO"),
                            aquadopp_temperature=record.get("Aquadopp Temperature"),
                            corrected_wind_direction=record.get(
                                "Corrected Wind Direction"
                            ),
                            corrected_wind_speed=record.get("Corrected Wind Speed"),
                            air_temperature=record.get("Air Temperature"),
                            relative_humidity=record.get("Relative Humidity"),
                            barometric_pressure=record.get("Barometric Pressure"),
                            precipitation_intensity=record.get(
                                "Precipitation Intensity"
                            ),
                            precipitation_total=record.get("Precipitation Total"),
                            wmo_average_wind_direction=record.get(
                                "WMO Average Wind Direction"
                            ),
                            wmo_average_wind_speed=record.get("WMO Average Wind Speed"),
                            latitude=record.get("Latitude"),
                            longitude=record.get("Longitude"),
                            vel_e_cell_1=record.get("vel_e_cell_1"),
                            vel_n_cell_1=record.get("vel_n_cell_1"),
                            vel_u_cell_1=record.get("vel_u_cell_1"),
                            current_speed_1=record.get("current_speed_1"),
                            current_direction_1=record.get("current_direction_1"),
                            vel_e_cell_2=record.get("vel_e_cell_2"),
                            vel_n_cell_2=record.get("vel_n_cell_2"),
                            vel_u_cell_2=record.get("vel_u_cell_2"),
                            current_speed_2=record.get("current_speed_2"),
                            current_direction_2=record.get("current_direction_2"),
                            vel_e_cell_3=record.get("vel_e_cell_3"),
                            vel_n_cell_3=record.get("vel_n_cell_3"),
                            vel_u_cell_3=record.get("vel_u_cell_3"),
                            current_speed_3=record.get("current_speed_3"),
                            current_direction_3=record.get("current_direction_3"),
                            vel_e_cell_4=record.get("vel_e_cell_4"),
                            vel_n_cell_4=record.get("vel_n_cell_4"),
                            vel_u_cell_4=record.get("vel_u_cell_4"),
                            current_speed_4=record.get("current_speed_4"),
                            current_direction_4=record.get("current_direction_4"),
                            vel_e_cell_5=record.get("vel_e_cell_5"),
                            vel_n_cell_5=record.get("vel_n_cell_5"),
                            vel_u_cell_5=record.get("vel_u_cell_5"),
                            current_speed_5=record.get("current_speed_5"),
                            current_direction_5=record.get("current_direction_5"),
                            vel_e_cell_6=record.get("vel_e_cell_6"),
                            vel_n_cell_6=record.get("vel_n_cell_6"),
                            vel_u_cell_6=record.get("vel_u_cell_6"),
                            current_speed_6=record.get("current_speed_6"),
                            current_direction_6=record.get("current_direction_6"),
                            vel_e_cell_7=record.get("vel_e_cell_7"),
                            vel_n_cell_7=record.get("vel_n_cell_7"),
                            vel_u_cell_7=record.get("vel_u_cell_7"),
                            current_speed_7=record.get("current_speed_7"),
                            current_direction_7=record.get("current_direction_7"),
                            vel_e_cell_8=record.get("vel_e_cell_8"),
                            vel_n_cell_8=record.get("vel_n_cell_8"),
                            vel_u_cell_8=record.get("vel_u_cell_8"),
                            current_speed_8=record.get("current_speed_8"),
                            current_direction_8=record.get("current_direction_8"),
                            vel_e_cell_9=record.get("vel_e_cell_9"),
                            vel_n_cell_9=record.get("vel_n_cell_9"),
                            vel_u_cell_9=record.get("vel_u_cell_9"),
                            current_speed_9=record.get("current_speed_9"),
                            current_direction_9=record.get("current_direction_9"),
                            vel_e_cell_10=record.get("vel_e_cell_10"),
                            vel_n_cell_10=record.get("vel_n_cell_10"),
                            vel_u_cell_10=record.get("vel_u_cell_10"),
                            current_speed_10=record.get("current_speed_10"),
                            current_direction_10=record.get("current_direction_10"),
                            time=combined_datetime,
                        )
                    )

                # Batch insert into database
                try:
                    BuoyData.objects.bulk_create(data_list)
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
