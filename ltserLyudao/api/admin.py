from django.contrib import admin
from .models import CoralData, MemorabiliaContent, LandUsage, OceanUsage, TemporalVariation

class CoralDataAdmin(admin.ModelAdmin):
    list_display = ('dataID', 'eventID', 'year', 'month', 'day', 'time', 'locationID', 'verbatimLocality', 'locality', 'verbatimDepth', 'decimalLatitude', 'decimalLongitude', 'replicate', 'scientificName', 'taxonRank', 'family', 'identificationRemarks', 'measurementType', 'measurementValue', 'measurementUnit', 'individualCount', 'recordedBy', 'identifiedBy', 'samplingProtocol', 'sampleSizeValue', 'sampleSizeUnit')
    search_fields = ['dataID', 'eventID', 'locality', 'scientificName']
    # 更多自定義設置...

class MemorabiliaContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'description')

class LandUsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'description', 'content')

class OceanUsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'description', 'content')

class TemporalVariationAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'description', 'content')

admin.site.register(CoralData, CoralDataAdmin)
admin.site.register(MemorabiliaContent, MemorabiliaContentAdmin)
admin.site.register(LandUsage, LandUsageAdmin)
admin.site.register(OceanUsage, OceanUsageAdmin)
admin.site.register(TemporalVariation, TemporalVariationAdmin)
