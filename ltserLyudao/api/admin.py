from django.contrib import admin
from .models import CoralData

class CoralDataAdmin(admin.ModelAdmin):
    list_display = ('dataID', 'eventID', 'year', 'month', 'day', 'time', 'locationID', 'verbatimLocality', 'locality', 'verbatimDepth', 'decimalLatitude', 'decimalLongitude', 'replicate', 'scientificName', 'taxonRank', 'family', 'identificationRemarks', 'measurementType', 'measurementValue', 'measurementUnit', 'individualCount', 'recordedBy', 'identifiedBy', 'samplingProtocol', 'sampleSizeValue', 'sampleSizeUnit')
    search_fields = ['dataID', 'eventID', 'locality', 'scientificName']
    # 更多自定義設置...

admin.site.register(CoralData, CoralDataAdmin)
