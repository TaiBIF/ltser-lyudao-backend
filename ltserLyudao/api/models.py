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