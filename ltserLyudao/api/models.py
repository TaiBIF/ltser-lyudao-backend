from django.db import models
import uuid


class WaterData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    resourceName = models.CharField(max_length=255)
    time = models.DateField()
    locationID = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    verbatimDepth = models.FloatField(null=True, blank=True)
    waterTemperature = models.FloatField(null=True, blank=True)
    conductivity = models.FloatField(null=True, blank=True)
    salinity = models.FloatField(null=True, blank=True)
    turbidity = models.FloatField(null=True, blank=True)
    SS = models.FloatField(null=True, blank=True)
    NH3_H = models.FloatField(null=True, blank=True)
    NO2_H = models.FloatField(null=True, blank=True)
    NO3_H = models.FloatField(null=True, blank=True)
    PO4_P = models.FloatField(null=True, blank=True)
    TBC = models.FloatField(null=True, blank=True)
    vibrio = models.FloatField(null=True, blank=True)
    COD = models.FloatField(null=True, blank=True)
    MBAS = models.FloatField(null=True, blank=True)
    TOC = models.FloatField(null=True, blank=True)
    Lipid = models.FloatField(null=True, blank=True)
    BOD5 = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "WaterData"


class WeatherData(models.Model):
    dataID = models.CharField(max_length=255)
    resourceName = models.CharField(max_length=255)
    time = models.DateTimeField()
    locationID = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    stationAttribute = models.CharField(max_length=255)
    decimalLongitude = models.FloatField()
    decimalLatitude = models.FloatField()
    stationAddress = models.CharField(max_length=255)
    PAR = models.FloatField(null=True, blank=True)
    solarRadiation = models.FloatField(null=True, blank=True)
    windDirection = models.FloatField(null=True, blank=True)
    pressure = models.FloatField(null=True, blank=True)
    windSpeed = models.FloatField(null=True, blank=True)
    gustSpeed = models.FloatField(null=True, blank=True)
    airTemperature = models.FloatField(null=True, blank=True)
    RH = models.FloatField(null=True, blank=True)
    precipitation = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "WeatherData"


class HabitatData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    time = models.DateField()
    season = models.CharField(max_length=255)
    river = models.CharField(max_length=255)
    locationID = models.CharField(max_length=255)
    factor = models.CharField(max_length=255)
    score = models.IntegerField()
    samplingProtocol = models.CharField(max_length=255)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "HabitatData"


class BaseSeaTemperatureData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    resourceName = models.CharField(max_length=255)
    locationID = models.CharField(max_length=255)
    verbatimDepth = models.CharField(max_length=255)
    fieldNumber = models.CharField(max_length=255, null=True, blank=True)
    time = models.DateTimeField()
    seaTemperature = models.FloatField(null=True)

    def __str__(self):
        return self.dataID

    class Meta:
        abstract = True


class SeaTemperatureData(BaseSeaTemperatureData):
    class Meta:
        db_table = "SeaTemperatureData"


class SeaTemperatureCK2023(BaseSeaTemperatureData):
    class Meta:
        db_table = "SeaTemperatureCK2023"


class SeaTemperatureDBS2023(BaseSeaTemperatureData):
    class Meta:
        db_table = "SeaTemperatureDBS2023"


class SeaTemperatureGG2023(BaseSeaTemperatureData):
    class Meta:
        db_table = "SeaTemperatureGG2023"


class SeaTemperatureGW2023(BaseSeaTemperatureData):
    class Meta:
        db_table = "SeaTemperatureGW2023"


class SeaTemperatureNL2023(BaseSeaTemperatureData):
    class Meta:
        db_table = "SeaTemperatureNL2023"


class SeaTemperatureSL2023(BaseSeaTemperatureData):
    class Meta:
        db_table = "SeaTemperatureSL2023"


class SeaTemperatureWQG2023(BaseSeaTemperatureData):
    class Meta:
        db_table = "SeaTemperatureWQG2023"


class SeaTemperatureYZH2023(BaseSeaTemperatureData):
    class Meta:
        db_table = "SeaTemperatureYZH2023"


class SeaTemperatureZP2023(BaseSeaTemperatureData):
    class Meta:
        db_table = "SeaTemperatureZP2023"


class CoralData(models.Model):
    dataID = models.CharField(max_length=50)
    eventID = models.CharField(max_length=50)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    time = models.DateTimeField()
    locationID = models.CharField(max_length=50)
    verbatimLocality = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    verbatimDepth = models.CharField(max_length=50)
    decimalLatitude = models.DecimalField(max_digits=10, decimal_places=8)
    decimalLongitude = models.DecimalField(max_digits=11, decimal_places=8)
    replicate = models.IntegerField()
    scientificName = models.CharField(max_length=50)
    taxonRank = models.CharField(max_length=50)
    family = models.CharField(max_length=50)
    identificationRemarks = models.CharField(max_length=50, blank=True, null=True)
    measurementType = models.CharField(max_length=50)
    measurementValue = models.FloatField()
    measurementUnit = models.CharField(max_length=50)
    individualCount = models.IntegerField()
    recordedBy = models.CharField(max_length=50)
    identifiedBy = models.CharField(max_length=50)
    samplingProtocol = models.CharField(max_length=50)
    sampleSizeValue = models.FloatField()
    sampleSizeUnit = models.CharField(max_length=50)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "CoralData"


class CoralCommData(models.Model):
    dataID = models.CharField(max_length=50)
    eventID = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    time = models.DateField(null=True, blank=True)
    locationID = models.CharField(max_length=50, null=True, blank=True)
    verbatimLocality = models.CharField(max_length=50, null=True, blank=True)
    locality = models.CharField(max_length=50, null=True, blank=True)
    verbatimDepth = models.CharField(max_length=50, null=True, blank=True)
    decimalLatitude = models.DecimalField(
        max_digits=10, decimal_places=8, null=True, blank=True
    )
    decimalLongitude = models.DecimalField(
        max_digits=11, decimal_places=8, null=True, blank=True
    )
    replicate = models.CharField(max_length=255, null=True, blank=True)
    Benthic_group = models.CharField(max_length=255, null=True, blank=True)
    Benthic_subgroup = models.CharField(max_length=255, null=True, blank=True)
    coverInPercentage = models.FloatField(null=True, blank=True)
    Field_codes_on_CPCe = models.CharField(max_length=255, null=True, blank=True)
    samplingProtocol = models.CharField(max_length=255, null=True, blank=True)
    sampleSizeValue = models.IntegerField(null=True, blank=True)
    sampleSizeUnit = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "CoralCommData"


class PlantData(models.Model):
    dataID = models.CharField(max_length=100)
    eventID = models.CharField(max_length=100, null=True, blank=True)
    time = models.DateField(null=True, blank=True)
    locationID = models.CharField(max_length=50, null=True, blank=True)
    habitat = models.CharField(max_length=50, null=True, blank=True)
    samplingProtocol = models.CharField(max_length=50, null=True, blank=True)
    sampleSizeValue = models.IntegerField(null=True, blank=True)
    sampleSizeUnit = models.CharField(max_length=50, null=True, blank=True)
    decimalLatitude = models.FloatField(null=True, blank=True)
    decimalLongitude = models.FloatField(null=True, blank=True)
    coordinatePrecision = models.FloatField(null=True, blank=True)
    verbatimElevation = models.CharField(max_length=50, null=True, blank=True)
    family = models.CharField(max_length=50, null=True, blank=True)
    scientificName = models.CharField(max_length=200, null=True, blank=True)
    vernacularName = models.CharField(max_length=50, null=True, blank=True)
    taxonRank = models.CharField(max_length=50, null=True, blank=True)
    recordedBy = models.CharField(max_length=50, null=True, blank=True)
    identifiedBy = models.CharField(max_length=50, null=True, blank=True)
    measurementType = models.CharField(max_length=50, null=True, blank=True)
    measurementValue = models.FloatField(null=True, blank=True)
    measurementUnit = models.CharField(max_length=50, null=True, blank=True)
    layer = models.CharField(max_length=50, null=True, blank=True)
    measurementDeterminedDate = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "PlantData"


class BirdNetSoundData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255, null=True, blank=True)
    locationID = models.CharField(max_length=10, null=True, blank=True)
    species_list = models.CharField(
        max_length=255, null=True, blank=True
    )  # Use None for no species
    scientificName = models.CharField(max_length=255, null=True, blank=True)
    taxonRank = models.CharField(max_length=255, null=True, blank=True)
    vernacularName = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    time_begin = models.IntegerField(null=True, blank=True)
    time_end = models.IntegerField(null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    associatedMedia = models.CharField(max_length=255, null=True, blank=True)
    week = models.IntegerField(null=True, blank=True)
    overlap = models.IntegerField(null=True, blank=True)
    sensitivity = models.IntegerField(null=True, blank=True)
    min_conf = models.FloatField(null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "BirdNetSoundData"


class BaseBirdNetSoundData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    species_list = models.CharField(
        max_length=255, null=True, blank=True
    )  # Use None for no species
    scientificName = models.CharField(max_length=255)
    taxonRank = models.CharField(max_length=255)
    vernacularName = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    time_begin = models.IntegerField()
    time_end = models.IntegerField()
    confidence = models.FloatField()
    associatedMedia = models.CharField(max_length=255)
    week = models.IntegerField()
    overlap = models.IntegerField()
    sensitivity = models.IntegerField()
    min_conf = models.FloatField()
    time = models.DateTimeField()

    def __str__(self):
        return self.dataID

    class Meta:
        abstract = True


class BirdNetSoundBS2023(BaseBirdNetSoundData):
    class Meta:
        db_table = "BirdNetSoundBS2023"


class BirdNetSoundGST2023(BaseBirdNetSoundData):
    class Meta:
        db_table = "BirdNetSoundGST2023"


class BirdNetSoundLH2023(BaseBirdNetSoundData):
    class Meta:
        db_table = "BirdNetSoundLH2023"


class BirdNetSoundYZH2023(BaseBirdNetSoundData):
    class Meta:
        db_table = "BirdNetSoundYZH2023"


class FishData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255, null=True, blank=True)
    time = models.DateField(null=True, blank=True)
    season = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    locationID = models.CharField(max_length=255, null=True, blank=True)
    locality = models.CharField(max_length=255, null=True, blank=True)
    verbatimDepth = models.CharField(max_length=255, null=True, blank=True)
    replicate = models.IntegerField(null=True, blank=True)
    sampleSizeValue = models.IntegerField(null=True, blank=True)
    sampleSizeUnit = models.CharField(max_length=255, null=True, blank=True)
    fieldNotes = models.CharField(max_length=255, null=True, blank=True)
    recordedBy = models.CharField(max_length=255, null=True, blank=True)
    family = models.CharField(max_length=255, null=True, blank=True)
    scientificName = models.CharField(max_length=255, null=True, blank=True)
    taxonRank = models.CharField(max_length=255, null=True, blank=True)
    bodyLength = models.FloatField(null=True, blank=True)
    samplingProtocol = models.CharField(max_length=255, null=True, blank=True)
    individualCount = models.IntegerField(null=True, blank=True)
    identifiedBy = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "FishData"


class FishingData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    time = models.DateTimeField()
    locationID = models.CharField(max_length=255)
    verbatimLocality = models.CharField(max_length=255)
    is_local_villager = models.CharField(max_length=255)
    purpose = models.CharField(max_length=255, null=True, blank=True)
    preferable_site = models.CharField(max_length=255, null=True, blank=True)
    catchment_individuals_per_month = models.CharField(
        max_length=255, null=True, blank=True
    )
    fishing_feq = models.CharField(max_length=255, null=True, blank=True)
    fishing_method = models.CharField(max_length=255, null=True, blank=True)
    bait = models.CharField(max_length=255, null=True, blank=True)
    fish_species = models.CharField(max_length=2550, null=True, blank=True)
    feel_size_decrease = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "FishingData"


class ZoobenthosData(models.Model):
    dataID = models.CharField(max_length=100, null=True, blank=True)
    eventID = models.CharField(max_length=100, null=True, blank=True)
    time = models.DateField(null=True, blank=True)
    season = models.CharField(max_length=50, null=True, blank=True)
    day_or_night = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    river = models.CharField(max_length=100, null=True, blank=True)
    locationID = models.CharField(max_length=10, null=True, blank=True)
    surveyObjectID = models.CharField(max_length=10, null=True, blank=True)
    surveyObject = models.CharField(max_length=100, null=True, blank=True)
    phylum = models.CharField(max_length=100, null=True, blank=True)
    phylum_c = models.CharField(max_length=100, null=True, blank=True)
    class_name = models.CharField(
        max_length=100, null=True, blank=True
    )  # 使用 class_name 作為欄位名稱
    class_c = models.CharField(max_length=100, null=True, blank=True)
    family = models.CharField(max_length=100, null=True, blank=True)
    family_c = models.CharField(max_length=100, null=True, blank=True)
    scientificName = models.CharField(max_length=100, null=True, blank=True)
    vernacularName = models.CharField(max_length=100, null=True, blank=True)
    taxonRank = models.CharField(max_length=50, null=True, blank=True)
    individualCount = models.IntegerField(null=True, blank=True)
    samplingProtocol = models.CharField(max_length=100, null=True, blank=True)
    habitat = models.CharField(max_length=100, null=True, blank=True)
    informationWithheld = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "ZoobenthosData"


class TerreSoundIndexData(models.Model):
    dataID = models.CharField(max_length=200)
    eventID = models.CharField(max_length=200, null=True, blank=True)
    locationID = models.CharField(max_length=10, null=True, blank=True)
    sh = models.FloatField(null=True, blank=True)
    th = models.FloatField(null=True, blank=True)
    H = models.FloatField(null=True, blank=True)
    ACI = models.FloatField(null=True, blank=True)
    ADI = models.FloatField(null=True, blank=True)
    AEI = models.FloatField(null=True, blank=True)
    BI = models.FloatField(null=True, blank=True)
    NDSI = models.FloatField(null=True, blank=True)
    associatedMedia = models.CharField(max_length=200, null=True, blank=True)
    min = models.FloatField(null=True, blank=True)
    sec = models.FloatField(null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "TerreSoundIndexData"


class BaseTerreSoundIndexData(models.Model):
    id = models.AutoField(primary_key=True)
    dataID = models.CharField(max_length=200)
    eventID = models.CharField(max_length=200)
    sh = models.FloatField()
    th = models.FloatField()
    H = models.FloatField()
    ACI = models.FloatField()
    ADI = models.FloatField()
    AEI = models.FloatField()
    BI = models.FloatField()
    NDSI = models.FloatField()
    associatedMedia = models.CharField(max_length=200)
    min = models.FloatField()
    sec = models.FloatField()
    time = models.DateTimeField()

    def __str__(self):
        return self.dataID

    class Meta:
        abstract = True


class TerreSoundIndexBS2023(BaseTerreSoundIndexData):
    class Meta:
        db_table = "TerreSoundIndexBS2023"


class TerreSoundIndexGST2023(BaseTerreSoundIndexData):
    class Meta:
        db_table = "TerreSoundIndexGST2023"


class TerreSoundIndexLH2023(BaseTerreSoundIndexData):
    class Meta:
        db_table = "TerreSoundIndexLH2023"


class TerreSoundIndexYZH2023(BaseTerreSoundIndexData):
    class Meta:
        db_table = "TerreSoundIndexYZH2023"


class OceanSoundIndexData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255, null=True, blank=True)
    locationID = models.CharField(max_length=10, null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)
    kHz0_24 = models.FloatField(null=True, blank=True)
    lower_200Hz = models.FloatField(null=True, blank=True)
    Hz200_1500 = models.FloatField(null=True, blank=True)
    higher_1500Hz = models.FloatField(null=True, blank=True)
    verbatimDepth = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "OceanSoundIndexData"


class BioSoundData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255, null=True, blank=True)
    locationID = models.CharField(max_length=10, null=True, blank=True)
    classid = models.IntegerField(null=True, blank=True)
    scientificName = models.CharField(max_length=255, null=True, blank=True)
    taxonRank = models.CharField(max_length=255, null=True, blank=True)
    vernacularName = models.CharField(max_length=255, null=True, blank=True)
    soundclass = models.CharField(max_length=255, null=True, blank=True)
    time_begin = models.IntegerField(null=True, blank=True)
    time_end = models.IntegerField(null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    associatedMedia = models.CharField(max_length=255, null=True, blank=True)
    freq_low = models.IntegerField(null=True, blank=True)
    freq_high = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "BioSoundData"


class BaseBioSoundData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    classid = models.IntegerField()
    scientificName = models.CharField(max_length=255)
    taxonRank = models.CharField(max_length=255)
    vernacularName = models.CharField(max_length=255)
    soundclass = models.CharField(max_length=255)
    time_begin = models.IntegerField()
    time_end = models.IntegerField()
    confidence = models.FloatField()
    associatedMedia = models.CharField(max_length=255)
    freq_low = models.IntegerField()
    freq_high = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.dataID

    class Meta:
        abstract = True


class BioSoundYZH2023(BaseBioSoundData):
    class Meta:
        db_table = "BioSoundYZH2023"


class BioSoundLH2023(BaseBioSoundData):
    class Meta:
        db_table = "BioSoundLH2023"


class BioSoundGST2023(BaseBioSoundData):
    class Meta:
        db_table = "BioSoundGST2023"


class BioSoundBS2023(BaseBioSoundData):
    class Meta:
        db_table = "BioSoundBS2023"


class AquaticfaunaData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255, null=True, blank=True)
    time = models.DateField(null=True, blank=True)
    season = models.CharField(max_length=50, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    river = models.CharField(max_length=255, null=True, blank=True)
    locationID = models.CharField(max_length=50, null=True, blank=True)
    surveyObjectID = models.CharField(max_length=255, null=True, blank=True)
    surveyObject = models.CharField(max_length=255, null=True, blank=True)
    phylum = models.CharField(max_length=255, null=True, blank=True)
    phylum_c = models.CharField(max_length=255, null=True, blank=True)
    class_field = models.CharField(
        max_length=255, db_column="class", null=True, blank=True
    )
    class_c = models.CharField(max_length=255, null=True, blank=True)
    family = models.CharField(max_length=255, null=True, blank=True)
    family_c = models.CharField(max_length=255, null=True, blank=True)
    scientificName = models.CharField(max_length=255, null=True, blank=True)
    vernacularName = models.CharField(max_length=255, null=True, blank=True)
    taxonRank = models.CharField(max_length=100, null=True, blank=True)
    individualCount = models.IntegerField(null=True, blank=True)
    samplingProtocol = models.CharField(max_length=255, null=True, blank=True)
    abundance = models.FloatField(null=True, blank=True)
    abundanceUnit = models.CharField(max_length=100, null=True, blank=True)
    informationWithheld = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "AquaticfaunaData"


class StreamData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    time = models.DateField()
    locationID = models.CharField(max_length=50)
    locality = models.CharField(max_length=255)
    waterTemperature = models.FloatField(null=True, blank=True)
    pH = models.FloatField(null=True, blank=True)
    DO = models.FloatField(null=True, blank=True)
    conductivity = models.FloatField(null=True, blank=True)
    salinity = models.FloatField(null=True, blank=True)
    SS = models.FloatField(null=True, blank=True)
    NH3_H = models.FloatField(null=True, blank=True)
    NO2_H = models.FloatField(null=True, blank=True)
    NO3_H = models.FloatField(null=True, blank=True)
    PO4_P = models.FloatField(null=True, blank=True)
    BOD5 = models.FloatField(null=True, blank=True)
    RPI_Score = models.FloatField(null=True, blank=True)
    RPI_Level = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "StreamData"


class OtolithData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    family = models.CharField(max_length=50)
    genus = models.CharField(max_length=50)
    scientificName = models.CharField(max_length=50)
    taxonRank = models.CharField(max_length=50)
    geologicalAge = models.CharField(max_length=50)
    locationID = models.CharField(max_length=50)
    locality = models.CharField(max_length=255)
    time = models.DateTimeField()
    samplingProtocol = models.CharField(max_length=255)
    typeStatus = models.CharField(max_length=50)
    recordNumber = models.CharField(max_length=255)
    recordedBy = models.CharField(max_length=50)
    identifiedBy = models.CharField(max_length=50)
    individualCount = models.IntegerField()
    verbatimDepth = models.FloatField()

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "OtolithData"


class CoralDivData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    time = models.DateTimeField()
    locationID = models.CharField(max_length=50)
    verbatimLocality = models.CharField(max_length=50)
    locality = models.CharField(max_length=255)
    decimalLatitude = models.FloatField()
    decimalLongitude = models.FloatField()
    verbatimDepth = models.FloatField()
    samplingProtocol = models.CharField(max_length=255)
    sampleSizeValue = models.FloatField()
    sampleSizeUnit = models.CharField(max_length=50)
    kingdom = models.CharField(max_length=50)
    phylum = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)  # 使用 class_name 作為欄位名稱
    family = models.CharField(max_length=100, null=True)
    genus = models.CharField(max_length=50)
    specificEpithet = models.CharField(max_length=50)
    occurrenceStatus = models.CharField(max_length=50)
    scientificName = models.CharField(max_length=50)
    taxonRank = models.CharField(max_length=50)
    abundance = models.FloatField()
    recordedBy = models.CharField(max_length=50)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "CoralDivData"


class CoralBleachData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    time = models.DateTimeField()
    locationID = models.CharField(max_length=50)
    verbatimLocality = models.CharField(max_length=50)
    locality = models.CharField(max_length=255)
    verbatimDepth = models.FloatField()
    decimalLatitude = models.FloatField()
    decimalLongitude = models.FloatField()
    replicate = models.IntegerField()
    scientificName = models.CharField(max_length=50)
    taxonRank = models.CharField(max_length=50)
    family = models.CharField(max_length=100, null=True)
    GrowthForm = models.CharField(max_length=50)
    measurementType = models.CharField(max_length=50)
    measurementValue = models.FloatField()
    measurementUnit = models.CharField(max_length=50)
    individualCount = models.IntegerField()
    recordedBy = models.CharField(max_length=50)
    identifiedBy = models.CharField(max_length=50)
    samplingProtocol = models.CharField(max_length=50)
    sampleSizeValue = models.FloatField()
    sampleSizeUnit = models.CharField(max_length=50)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = "CoralBleachData"


class LocationTableInfo(models.Model):
    location_id = models.CharField(max_length=10, unique=True)
    name_en = models.CharField(max_length=100)
    name_zh = models.CharField(max_length=100)

    def __str__(self):
        return self.location_id

    class Meta:
        db_table = "LocationTableInfo"


class BaseDataField(models.Model):
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=100)
    title_zh_tw = models.CharField(max_length=255)
    title_en = models.CharField(max_length=255)
    content_zh_tw = models.TextField(null=True, blank=True)
    content_en = models.TextField(null=True, blank=True)
    show = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.field_name


class CoralCommDataField(BaseDataField):

    class Meta:
        db_table = "CoralCommDataField"


class WaterDataField(BaseDataField):
    class Meta:
        db_table = "WaterDataField"


class WeatherDataField(BaseDataField):
    class Meta:
        db_table = "WeatherDataField"


class HabitatDataField(BaseDataField):
    class Meta:
        db_table = "HabitatDataField"


class SeaTemperatureDataField(BaseDataField):
    class Meta:
        db_table = "SeaTemperatureDataField"


class CoralDataField(BaseDataField):
    class Meta:
        db_table = "CoralDataField"


class FishDataField(BaseDataField):
    class Meta:
        db_table = "FishDataField"


class ZoobenthosDataField(BaseDataField):
    class Meta:
        db_table = "ZoobenthosDataField"


class PlantDataField(BaseDataField):
    class Meta:
        db_table = "PlantDataField"


class BirdNetSoundDataField(BaseDataField):
    class Meta:
        db_table = "BirdNetSoundDataField"


class FishingDataField(BaseDataField):
    class Meta:
        db_table = "FishingDataField"


class OceanSoundIndexDataField(BaseDataField):
    class Meta:
        db_table = "OceanSoundIndexDataField"


class BioSoundDataField(BaseDataField):
    class Meta:
        db_table = "BioSoundDataField"


class TerreSoundIndexDataField(BaseDataField):
    class Meta:
        db_table = "TerreSoundIndexDataField"


class AquaticfaunaDataField(BaseDataField):
    class Meta:
        db_table = "AquaticfaunaDataField"


class StreamDataField(BaseDataField):
    class Meta:
        db_table = "StreamDataField"


class OtolithDataField(BaseDataField):
    class Meta:
        db_table = "OtolithDataField"


class CoralDivDataField(BaseDataField):
    class Meta:
        db_table = "CoralDivDataField"


class CoralBleachDataField(BaseDataField):
    class Meta:
        db_table = "CoralBleachDataField"


class TBIADataField(BaseDataField):
    class Meta:
        db_table = "TBIADataField"


class MemorabiliaContent(models.Model):
    image = models.ImageField(upload_to="social_observation__images/")
    description = models.TextField()

    class Meta:
        db_table = "memorabilia_content"


class LandUsage(models.Model):
    image = models.ImageField(
        upload_to="social_observation__images/", null=True, blank=True, default=None
    )
    description = models.TextField(null=True, blank=True, default=None)
    content = models.TextField(null=True, blank=True, default=None)

    class Meta:
        db_table = "land_usage"


class OceanUsage(models.Model):
    image = models.ImageField(
        upload_to="social_observation__images/", null=True, blank=True, default=None
    )
    description = models.TextField(null=True, blank=True, default=None)
    content = models.TextField(null=True, blank=True, default=None)

    class Meta:
        db_table = "ocean_usage"


class TemporalVariation(models.Model):
    image = models.ImageField(
        upload_to="social_observation__images/", null=True, blank=True, default=None
    )
    description = models.TextField(null=True, blank=True, default=None)
    content = models.TextField(null=True, blank=True, default=None)

    class Meta:
        db_table = "temporal_variation"


class SocialInterview(models.Model):
    dataID = models.CharField(max_length=255)
    time = models.TextField()
    text = models.TextField(null=True, blank=True, default=None)
    CAP_issue = models.CharField(max_length=255, null=True, blank=True)
    local_issue = models.CharField(max_length=255, null=True, blank=True)
    tag = models.CharField(max_length=255, null=True, blank=True)
    participant_type = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "social_interview"


class SocialInterviewCapIssues(models.Model):
    cap_issue = models.CharField(max_length=255, null=True, blank=True)
    cap_issue_mandarin = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "social_interview_cap_issues"


class DatasetSummary(models.Model):
    datasetID = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    datasetName = models.CharField(max_length=255, null=True, blank=True)
    datasetStartDate = models.DateField(null=True, blank=True)
    datasetEndDate = models.DateField(null=True, blank=True)
    occurrenceCount = models.IntegerField(null=True, blank=True)
    resourceContacts = models.CharField(max_length=255, null=True, blank=True)
    datasetLicense = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateField(null=True, blank=True)
    modified = models.DateField(null=True, blank=True)
    datasetURL = models.URLField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = "dataset_summary"
