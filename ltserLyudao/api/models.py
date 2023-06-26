from django.db import models

class WeatherData(models.Model):
    dataID = models.CharField(max_length=255)
    resourceName = models.CharField(max_length=255)
    eventDate = models.DateTimeField()
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

class BaseSeaTemperatureData(models.Model):
    dataID = models.CharField(max_length=255)
    eventID = models.CharField(max_length=255)
    resourceName = models.CharField(max_length=255)
    locationID = models.CharField(max_length=255)
    verbatimDepth = models.CharField(max_length=255)
    fieldNumber = models.IntegerField(null=True)
    measurementDeterminedDate = models.DateTimeField()
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
    eventDate = models.DateTimeField()
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

class PlantData(models.Model):
    dataID = models.CharField(max_length=50)
    eventID = models.CharField(max_length=50)
    eventDate = models.DateTimeField()
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


from django.db import models

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
    measurementDeterminedDate = models.DateTimeField()

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