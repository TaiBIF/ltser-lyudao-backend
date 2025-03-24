import requests
import uuid
from datetime import datetime
from api.utils.validate import validate_integer, validate_date, validate_decimal
from api.models import (
    DatasetSummary,
    CoralDivData,
    CoralBleachData,
    CoralData,
    ZoobenthosData,
    PlantData,
    BirdNetSoundData,
    BioSoundData,
    FishData,
    AquaticfaunaData,
    OtolithData,
)
from django.db import connection
from django.db.models import Min, Max

MODEL_CONFIG = {
    "ltser-lyudao-coraldiv": {
        "short_name": "coral-div",
        "model_name": CoralDivData,
    },
    "ltser-lyudao-coralbleach": {
        "short_name": "coral-bleach",
        "model_name": CoralBleachData,
    },
    "ltser-lyudao-coraljuv": {
        "short_name": "coral-rec",
        "model_name": CoralData,
    },
    "ltser-lyudao-zoobenthos": {
        "short_name": "zoobenthos",
        "model_name": ZoobenthosData,
    },
    "ltser-lyudao-plant": {
        "short_name": "plant",
        "model_name": PlantData,
    },
    "ltser-lyudao-birdnetsound": {
        "short_name": "bird-net-sound",
        "model_name": BirdNetSoundData,
    },
    "ltser-lyudao-biosound": {
        "short_name": "bio-sound",
        "model_name": BioSoundData,
    },
    "ltser-lyudao-fishdiv": {
        "short_name": "fish-div",
        "model_name": FishData,
    },
    "ltser-lyudao-aquaticfauna": {
        "short_name": "aquaticfauna",
        "model_name": AquaticfaunaData,
    },
    "ltser-lyudao-otolith": {
        "short_name": "otolith",
        "model_name": OtolithData,
    },
}

current_date = datetime.now().isoformat()
print("-" * 60)
print(f"Execution date: {current_date}")
print("Database: DatasetSummary")

metadata_list = [
    "ltser-lyudao-fishdiv",
    "ltser-lyudao-aquaticfauna",
    "ltser-lyudao-otolith",
    "ltser-lyudao-coraldiv",
    "ltser-lyudao-coraljuv",
    "ltser-lyudao-coralbleach",
    "ltser-lyudao-zoobenthos",
    "ltser-lyudao-plant",
    "ltser-lyudao-birdnetsound",
    "ltser-lyudao-biosound",
]
data_list = []

for dataset_name in metadata_list:
    metadata_url = (
        f"https://data.depositar.io/api/3/action/package_show?id={dataset_name}"
    )
    response = requests.get(metadata_url)

    if response.status_code == 200:
        print(
            f"Successfully fetched metadata from API. Status code: {response.status_code}"
        )

        table_short_name = MODEL_CONFIG[dataset_name]["short_name"]
        model_name = MODEL_CONFIG[dataset_name]["model_name"]

        date_range = model_name.objects.aggregate(
            earliest_eventDate=Min("time"),
            latest_eventDate=Max("time"),
        )

        dataset_url = f"https://ltsertwlyudao.org/site-data/ecological-observation/{table_short_name}"

        previous_datasetID = (
            DatasetSummary.objects.filter(datasetName=table_short_name)
            .values_list("datasetID", flat=True)
            .first()
        )

        data = response.json()
        author = data.get("result").get("author")
        metadata_modified = data.get("result").get("metadata_modified")

        datasetID = (
            previous_datasetID or uuid.uuid4()
        )  # 有 previous_datasetID 的話繼續用，沒有的話新建一個 uuid
        datasetName = table_short_name
        datasetStartDate = date_range["earliest_eventDate"]
        datasetEndDate = date_range["latest_eventDate"]
        occurrenceCount = model_name.objects.count()
        resourceContacts = author
        datasetLicense = "CC-BY 4.0"
        created = validate_date(
            metadata_modified, "metadata_modified", table_short_name
        )
        modified = validate_date(current_date, "current_date", table_short_name)
        datasetURL = dataset_url

        data_list.append(
            DatasetSummary(
                datasetID=datasetID,
                datasetName=datasetName,
                datasetStartDate=datasetStartDate,
                datasetEndDate=datasetEndDate,
                occurrenceCount=occurrenceCount,
                resourceContacts=resourceContacts,
                datasetLicense=datasetLicense,
                created=created,
                modified=modified,
                datasetURL=datasetURL,
            )
        )
    else:
        print(
            f"ERROR: Depositar API {dataset_name} status code, {response.status_code}"
        )
        exit()

try:
    table_name = DatasetSummary._meta.db_table
    with connection.cursor() as cursor:
        cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")
    print("Action: Successfully truncated table")
except Exception as e:
    print(f"ERROR: Failed to truncate table. Exception: {e}")
    exit(1)

try:
    DatasetSummary.objects.bulk_create(data_list)
except Exception as e:
    print(
        f"ERROR: Failed to insert records for resource {dataset_name}. Exception: {e}"
    )
