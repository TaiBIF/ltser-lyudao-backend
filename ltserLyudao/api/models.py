from django.db import models

class WaterData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    resourceName = models.CharField(max_length=255)
    time = models.DateField()
    locationID = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    verbatimDepth = models.FloatField()
    waterTemperature = models.FloatField()
    DO = models.FloatField(null=True, blank=True)
    conductivity = models.FloatField()
    salinity = models.FloatField()
    turbidity = models.FloatField()
    SS = models.FloatField()
    NH3_H = models.FloatField()
    NO2_H = models.FloatField()
    NO3_H = models.FloatField()
    PO4_P = models.FloatField()
    TBC = models.FloatField()
    vibrio = models.FloatField(null=True, blank=True)
    COD = models.FloatField(null=True, blank=True)
    MBAS = models.FloatField(null=True, blank=True)
    TOC = models.FloatField(null=True, blank=True)
    lipid = models.FloatField(null=True, blank=True)
    BOD5 = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = 'WaterData'


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
    PAR = models.FloatField()
    solarRadiation = models.FloatField()
    windDirection = models.IntegerField()
    pressure = models.FloatField()
    windSpeed = models.FloatField(null=True)
    gustSpeed = models.FloatField(null=True)
    airTemperature = models.FloatField(null=True)
    RH = models.FloatField(null=True)
    precipitation = models.FloatField(null=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = 'WeatherData'

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
        db_table = 'HabitatData'

class BaseSeaTemperatureData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    resourceName = models.CharField(max_length=255)
    locationID = models.CharField(max_length=255)
    verbatimDepth = models.CharField(max_length=255)
    fieldNumber = models.IntegerField(null=True)
    time = models.DateTimeField()
    seaTemperature = models.FloatField(null=True)

    def __str__(self):
        return self.dataID

    class Meta:
        abstract = True

class SeaTemperatureCK2023(BaseSeaTemperatureData):
    class Meta:
        db_table = 'SeaTemperatureCK2023'

class SeaTemperatureDBS2023(BaseSeaTemperatureData):
    class Meta:
        db_table = 'SeaTemperatureDBS2023'

class SeaTemperatureGG2023(BaseSeaTemperatureData):
    class Meta:
        db_table = 'SeaTemperatureGG2023'

class SeaTemperatureGW2023(BaseSeaTemperatureData):
    class Meta:
        db_table = 'SeaTemperatureGW2023'

class SeaTemperatureNL2023(BaseSeaTemperatureData):
    class Meta:
        db_table = 'SeaTemperatureNL2023'

class SeaTemperatureSL2023(BaseSeaTemperatureData):
    class Meta:
        db_table = 'SeaTemperatureSL2023'

class SeaTemperatureWQG2023(BaseSeaTemperatureData):
    class Meta:
        db_table = 'SeaTemperatureWQG2023'

class SeaTemperatureYZH2023(BaseSeaTemperatureData):
    class Meta:
        db_table = 'SeaTemperatureYZH2023'

class SeaTemperatureZP2023(BaseSeaTemperatureData):
    class Meta:
        db_table = 'SeaTemperatureZP2023'

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
    decimalLongitude = models.DecimalField(max_digits=10, decimal_places=8)
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
        db_table = 'CoralData'

class CoralCommData(models.Model):
    dataID = models.CharField(max_length=50)
    eventID = models.CharField(max_length=50)
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    time = models.DateField()
    locationID = models.CharField(max_length=50)
    verbatimLocality = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    verbatimDepth = models.CharField(max_length=50)
    decimalLatitude = models.DecimalField(max_digits=10, decimal_places=8)
    decimalLongitude = models.DecimalField(max_digits=10, decimal_places=8)
    replicate = models.CharField(max_length=255)
    Benthic_group = models.CharField(max_length=255)
    Benthic_subgroup = models.CharField(max_length=255)
    coverInPercentage = models.FloatField()
    Field_codes_on_CPCe = models.CharField(max_length=255)
    samplingProtocol = models.CharField(max_length=255)
    sampleSizeValue = models.IntegerField()
    sampleSizeUnit = models.CharField(max_length=50)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = 'CoralCommData'

class PlantData(models.Model):
    dataID = models.CharField(max_length=50)
    eventID = models.CharField(max_length=50)
    time = models.DateTimeField()
    locationID = models.IntegerField()
    habitat = models.CharField(max_length=50)
    samplingProtocol = models.CharField(max_length=50)
    sampleSizeValue = models.IntegerField()
    sampleSizeUnit = models.CharField(max_length=50)
    decimalLatitude = models.FloatField()
    decimalLongitude = models.FloatField()
    coordinatePrecision = models.FloatField()
    verbatimElevation = models.CharField(max_length=50)
    family = models.CharField(max_length=50)
    scientificName = models.CharField(max_length=50)
    vernacularName = models.CharField(max_length=50)
    taxonRank = models.CharField(max_length=50)
    recordedBy = models.CharField(max_length=50)
    identifiedBy = models.CharField(max_length=50)
    measurementType = models.CharField(max_length=50)
    measurementValue = models.FloatField()
    measurementUnit = models.CharField(max_length=50)
    layer = models.CharField(max_length=50)
    measurementDeterminedDate = models.DateTimeField()

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = 'PlantData'


class BaseBirdNetSoundData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    species_list = models.CharField(max_length=255, null=True, blank=True)  # Use None for no species
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
        db_table = 'BirdNetSoundBS2023'

class BirdNetSoundGST2023(BaseBirdNetSoundData):
    class Meta:
        db_table = 'BirdNetSoundGST2023'

class BirdNetSoundLH2023(BaseBirdNetSoundData):
    class Meta:
        db_table = 'BirdNetSoundLH2023'

class BirdNetSoundYZH2023(BaseBirdNetSoundData):
    class Meta:
        db_table = 'BirdNetSoundYZH2023'


class FishData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    time =  models.DateTimeField()
    season = models.CharField(max_length=255)
    year = models.IntegerField()
    region = models.CharField(max_length=255)
    locationID = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    verbatimDepth = models.CharField(max_length=255)
    replicate = models.IntegerField()
    sampleSizeValue = models.IntegerField()
    sampleSizeUnit = models.CharField(max_length=255)
    fieldNotes = models.CharField(max_length=255)
    recordedBy = models.CharField(max_length=255)
    family = models.CharField(max_length=255)
    scientificName = models.CharField(max_length=255)
    taxonRank = models.CharField(max_length=255)
    bodyLength = models.FloatField()
    samplingProtocol = models.CharField(max_length=255)
    individualCount = models.IntegerField()
    identifiedBy = models.CharField(max_length=255)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = 'FishData'

class ZoobenthosData(models.Model):
    dataID = models.CharField(max_length=100)
    eventID = models.CharField(max_length=100)
    time = models.DateField()
    season = models.CharField(max_length=50)
    day_or_night = models.CharField(max_length=50)
    year = models.IntegerField()
    month = models.IntegerField()
    river = models.CharField(max_length=100)
    locationID = models.CharField(max_length=10)
    surveyObjectID = models.CharField(max_length=10)
    surveyObject = models.CharField(max_length=100)
    phylum = models.CharField(max_length=100)
    phylum_c = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)  # 使用 class_name 作為欄位名稱
    class_c = models.CharField(max_length=100)
    family = models.CharField(max_length=100, null=True)
    family_c = models.CharField(max_length=100, null=True)
    scientificName = models.CharField(max_length=100, null=True)
    vernacularName = models.CharField(max_length=100, null=True)
    taxonRank = models.CharField(max_length=50, null=True)
    individualCount = models.IntegerField()
    samplingProtocol = models.CharField(max_length=100, null=True)
    habitat = models.CharField(max_length=100, null=True)
    informationWithheld = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.dataID

    class Meta:
        db_table = 'ZoobenthosData'

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
        db_table = 'TerreSoundIndexBS2023'

class TerreSoundIndexGST2023(BaseTerreSoundIndexData):
    class Meta:
        db_table = 'TerreSoundIndexGST2023'

class TerreSoundIndexLH2023(BaseTerreSoundIndexData):
    class Meta:
        db_table = 'TerreSoundIndexLH2023'

class TerreSoundIndexYZH2023(BaseTerreSoundIndexData):
    class Meta:
        db_table = 'TerreSoundIndexYZH2023'