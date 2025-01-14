import requests
from api.models import SocialInterview, SocialInterviewCapIssues
from django.db import connection

# Step 1: Fetch metadata from API
metadata_url = 'https://data.depositar.io/api/3/action/package_show?id=ltser-lyudao-issue'
response = requests.get(metadata_url)
resource_list = []
config_resource_id = None


if response.status_code == 200:
    print(f'Successfully fetched metadata from API. Status code: {response.status_code}')
    data = response.json()
    records = data.get('result', {}).get('resources', [])
    for record in records:
        file_format = record.get('format')
        resource_id = record.get('id')
        name = record.get('name')
        if file_format == 'CSV' and name != 'CAP_and_local_issues_config':
            resource_list.append(resource_id)
            print(f'Action: Add resource with ID: {resource_id} and format: {file_format}')
        elif file_format == 'CSV' and name == 'CAP_and_local_issues_config':
            config_resource_id = resource_id
            print(f'Action: Add configuration resource with ID: {resource_id} and format: {file_format}')
        else:
            print(f'ERROR: Resource with ID: {resource_id} is not in CSV format.')
else:
    print(f'ERROR: Depositar API status code, {response.status_code}')
    exit(1) 

# Step 2: Truncate table
try:
    updated_table = [SocialInterview, SocialInterviewCapIssues]
    for table in updated_table:
        table_name = table._meta.db_table
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;')
    # SocialInterview.objects.all().delete()
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
                    # time = validate_date(record.get('date'), 'date', record)

                    data_list.append(
                        SocialInterview(
                            dataID=record.get('dataID'),
                            time=record.get('date'),
                            text=record.get('text'),
                            CAP_issue=record.get('CAP_issue'),
                            local_issue=record.get('local_issue'),
                            tag=record.get('tag'),
                            participant_type=record.get('participant_type'),
                        )
                    )

                # Batch insert into database
                try:
                    SocialInterview.objects.bulk_create(data_list)
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

# Step 4: Update configuration
if config_resource_id:
    url = f'https://data.depositar.io/zh_Hant_TW/api/3/action/datastore_search?resource_id={config_resource_id}'
    total_count = False
    offset = 0
    limit = 100
    records_count = 0

    print(f'- Started parsing configuration resource: {resource}')
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
                if record.get('cap_issue') and record.get('cap_issue_Mandarin'):
                    cleaned_cap_issue = record.get('cap_issue').split('.', 1)[1].strip()

                    data_list.append(
                        SocialInterviewCapIssues(
                            cap_issue=cleaned_cap_issue,
                            cap_issue_mandarin=record.get('cap_issue_Mandarin'),
                        )
                    )

            # Batch insert into database
            try:
                SocialInterviewCapIssues.objects.bulk_create(data_list)
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