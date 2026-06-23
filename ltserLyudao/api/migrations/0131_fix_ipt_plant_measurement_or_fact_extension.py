from django.db import migrations, models


def copy_event_id_to_occurrence_id(apps, schema_editor):
    model = apps.get_model("api", "IptPlantMeasurementOrFactExtension")
    for row in model.objects.all().iterator():
        row.occurrenceID = row.eventID
        row.save(update_fields=["occurrenceID"])


def copy_occurrence_id_to_event_id(apps, schema_editor):
    model = apps.get_model("api", "IptPlantMeasurementOrFactExtension")
    for row in model.objects.all().iterator():
        row.eventID = row.occurrenceID
        row.save(update_fields=["eventID"])


class Migration(migrations.Migration):
    dependencies = [
        (
            "api",
            "0130_iptplantevent_iptplantmeasurementorfactextension_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="iptplantmeasurementorfactextension",
            name="occurrenceID",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.RunPython(
            copy_event_id_to_occurrence_id,
            copy_occurrence_id_to_event_id,
        ),
        migrations.AlterField(
            model_name="iptplantmeasurementorfactextension",
            name="occurrenceID",
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AddField(
            model_name="iptplantmeasurementorfactextension",
            name="measurementType",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="iptplantmeasurementorfactextension",
            name="measurementValue",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="iptplantmeasurementorfactextension",
            name="measurementUnit",
            field=models.CharField(default="", max_length=255),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="eventID",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="eventDate",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="samplingProtocol",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="sampleSizeValue",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="sampleSizeUnit",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="samplingEffort",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="locationID",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="country",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="countryCode",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="county",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="municipality",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="locality",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="verbatimLocality",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="decimalLatitude",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="decimalLongitude",
        ),
        migrations.RemoveField(
            model_name="iptplantmeasurementorfactextension",
            name="geodeticDatum",
        ),
    ]
