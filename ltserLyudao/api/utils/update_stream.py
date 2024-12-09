import requests
from api.utils.validate import validate_date, validate_decimal
from api.models import StreamData

# Step 1: Fetch metadata from API
metadata_url = 'https://data.depositar.io/api/3/action/package_show?id=ltser-lyudao-stream'
response = requests.get(metadata_url)
resource_list = []

if response.status_code == 200:
    print(f'Successfully fetched metadata from API. Status code: {response.status_code}')
    data = response.json()
    records = data.get('result', {}).get('resources', [])
    for record in records:
        file_format = record.get('format')
        resource_id = record.get('id')
        if file_format == 'CSV':
            resource_list.append(resource_id)
            print(f'Action: Add resource with ID: {resource_id} and format: {file_format}')
        else:
            print(f'ERROR: Resource with ID: {resource_id} is not in CSV format.')
else:
    print(f'ERROR: Depositar API status code, {response.status_code}')
    exit(1) 

# Step 2: Truncate table
try:
    StreamData.objects.all().delete()
    print('Action: Successfully truncated table')
except Exception as e:
    print(f'ERROR: Failed to truncate table. Exception: {e}')
    exit(1)

# Step 3: Start parsing resources
print('Resource Parsing Progress:')
if resource_list:
    for resource in resource_list:
        url = f'https://data.depositar.io/zh_Hant_TW/api/3/action/datastore_search?resource_id={resource}'
        total_count = False
        offset = 0
        limit = 100
        records_count = 0

        print(f'- Started parsing resource: {resource}')
        while not total_count:
            params = {
                'offset': offset,
                'limit': limit
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                records = data.get('result', {}).get('records', [])
                if not records:
                    print(f'ERROR: No records found for resource: {resource}')
                    break
                records_count += len(records)

                data_list = []
                for record in records:
                    # Data validation and extraction
                    time = validate_date(record.get('eventDate'), 'eventDate', record)
                    waterTemperature = validate_decimal(record.get('waterTemperature'), 'waterTemperature', record)
                    pH = validate_decimal(record.get('pH'), 'pH', record)
                    DO = validate_decimal(record.get('DO'), 'DO', record)
                    conductivity = validate_decimal(record.get('conductivity'), 'conductivity', record)
                    salinity = validate_decimal(record.get('salinity'), 'salinity', record)
                    SS = validate_decimal(record.get('SS'), 'SS', record)
                    NH3_H = validate_decimal(record.get('NH3-H'), 'NH3-H', record)
                    NO2_H = validate_decimal(record.get('NO2-H'), 'NO2-H', record)
                    NO3_H = validate_decimal(record.get('NO3-H'), 'NO3-H', record)
                    PO4_P = validate_decimal(record.get('PO4-P'), 'PO4-P', record)
                    BOD5 = validate_decimal(record.get('BOD5'), 'BOD5', record)
                    RPI_Score = validate_decimal(record.get('RPI_Score'), 'RPI_Score', record)

                    data_list.append(
                        StreamData(
                            dataID=record.get('dataID'),
                            eventID=record.get('eventID'),
                            time=time,
                            locationID=record.get('locationID'),
                            locality=record.get('locality'),
                            waterTemperature=waterTemperature,
                            pH=pH,
                            DO=DO,
                            SS=SS,
                            NH3_H=NH3_H,
                            NO2_H=NO2_H,
                            NO3_H=NO3_H,
                            PO4_P=PO4_P,
                            BOD5=BOD5,
                            RPI_Score=RPI_Score,
                            RPI_Level=record.get('RPI_Level'),
                        )
                    )

                # Batch insert into database
                try:
                    StreamData.objects.bulk_create(data_list)
                except Exception as e:
                    print(f'ERROR: Failed to insert records for resource {resource}. Exception: {e}')
                    break

                offset += limit

                # Check if all records have been processed
                if records_count >= data.get('result', {}).get('total'):
                    print(f'    - Action: Successfully inserted {records_count} records')
                    total_count = True
            else:
                print(f'ERROR: Failed to fetch records for resource {resource}. Status code: {response.status_code}')
                break
else:
    print('ERROR: No valid CSV resources found for parsing.')

print('All operations completed successfully.')
print('-' * 60)