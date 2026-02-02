import re
from api.importing.adapters.waterdata import WaterDataAdapter
from api.importing.adapters.plantdata import PlantDataAdapter
from api.importing.adapters.zoobenthosdata import ZoobenthosDataAdapter
from api.importing.adapters.terresoundindex import TerreSoundIndexDataAdapter
from api.importing.adapters.biosound import BioSoundDataAdapter
from api.importing.adapters.habitat import HabitatDataAdapter
from api.importing.adapters.streamdata import StreamDataAdapter
from api.importing.adapters.aquaticfauna import AquaticfaunaDataAdapter
from api.importing.adapters.buoy import BuoyDataAdapter
from api.importing.adapters.fishdiv import FishDivAdapter
from api.importing.adapters.coralcomm import CoralCommDataAdapter
from api.importing.adapters.coralrec import CoralRecDataAdapter
from api.importing.adapters.fishing import FishingDataAdapter
from api.importing.adapters.weather import WeatherDataAdapter
from api.importing.adapters.seatemperature import SeaTemperatureDataAdapter
from api.importing.adapters.birdnetsound import BirdNetSoundDataAdapter
from api.importing.adapters.oceanindex import OceanSoundIndexDataAdapter

ADAPTERS = {
    "ltser-lyudao-water": WaterDataAdapter,
    "ltser-lyudao-plant": PlantDataAdapter,
    "ltser-lyudao-zoobenthos": ZoobenthosDataAdapter,
    "ltser-lyudao-terresoundindex": TerreSoundIndexDataAdapter,
    "ltser-lyudao-biosound": BioSoundDataAdapter,
    "ltser-lyudao-habitat": HabitatDataAdapter,
    "ltser-lyudao-stream": StreamDataAdapter,
    "ltser-lyudao-aquaticfauna": AquaticfaunaDataAdapter,
    "ltser-lyudao-buoy": BuoyDataAdapter,
    "ltser-lyudao-fishdiv": FishDivAdapter,
    "ltser-lyudao-coralcomm": CoralCommDataAdapter,
    "ltser-lyudao-coraljuv": CoralRecDataAdapter,
    "ltser-lyudao-fishing": FishingDataAdapter,
    "ltser-lyudao-weather": WeatherDataAdapter,
    "ltser-lyudao-seatemperature": SeaTemperatureDataAdapter,
    "ltser-lyudao-birdnetsound": BirdNetSoundDataAdapter,
    "ltser-lyudao-oceansound": OceanSoundIndexDataAdapter,
}


def normalize_package_name(package_name: str) -> str:
    return re.sub(r"-\d{6}$", "", package_name)
