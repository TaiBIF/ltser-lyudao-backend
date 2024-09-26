import requests
from datetime import datetime
from api.utils.validate import validate_datetime, validate_integer
from api.models import BirdNetSoundData

current_date = datetime.now().isoformat()
print('-' * 60)
print(f'Execution date: {current_date}')
print('Database: BirdNetSoundData')

# Step 1: Fetch metadata from API
metadata_url = 'https://data.depositar.io/api/3/action/package_show?id=ltser-lyudao-birdnetsound'
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
    BirdNetSoundData.objects.all().delete()
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
                    time = validate_datetime(record.get('measurementDeterminedDate'), 'measurementDeterminedDate', record)
                    time_begin = validate_integer(record.get('time_begin'), 'time_begin', record)
                    time_end = validate_integer(record.get('time_end'), 'time_end', record)
                    week = validate_integer(record.get('week'), 'week', record)
                    overlap = validate_integer(record.get('overlap'), 'overlap', record)
                    sensitivity = validate_integer(record.get('sensitivity'), 'sensitivity', record)

                    data_list.append(
                        BirdNetSoundData(
                            dataID=record.get('dataID'),         
                            eventID=record.get('eventID'),
                            locationID=record.get('locationID'),
                            species_list=record.get('species_list'),
                            scientificName=record.get('scientificName'),
                            taxonRank=record.get('taxonRank'),
                            vernacularName=record.get('vernacularName'),
                            model=record.get('model'),
                            time_begin=time_begin,
                            time_end=time_end,
                            confidence=record.get('confidence'),
                            associatedMedia=record.get('associatedMedia'),
                            week=week,
                            overlap=overlap,
                            sensitivity=sensitivity,
                            min_conf=record.get('min_conf'),
                            time=time,
                        )
                    )

                # Batch insert into database
                try:
                    BirdNetSoundData.objects.bulk_create(data_list)
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
