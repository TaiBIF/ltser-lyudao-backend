# Generated by Django 4.1.1 on 2024-08-27 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0051_coraldivdata_coraldivdatafield'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoralBleachData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataID', models.CharField(max_length=255)),
                ('eventID', models.CharField(max_length=255)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('locationID', models.CharField(max_length=50)),
                ('verbatimLocality', models.CharField(max_length=50)),
                ('locality', models.CharField(max_length=255)),
                ('verbatimDepth', models.FloatField()),
                ('decimalLatitude', models.FloatField()),
                ('decimalLongitude', models.FloatField()),
                ('replicate', models.IntegerField()),
                ('scientificName', models.CharField(max_length=50)),
                ('taxonRank', models.CharField(max_length=50)),
                ('family', models.CharField(max_length=100, null=True)),
                ('GrowthForm', models.CharField(max_length=50)),
                ('measurementType', models.CharField(max_length=50)),
                ('measurementValue', models.FloatField()),
                ('measurementUnit', models.CharField(max_length=50)),
                ('individualCount', models.IntegerField()),
                ('recordedBy', models.CharField(max_length=50)),
                ('identifiedBy', models.CharField(max_length=50)),
                ('samplingProtocol', models.CharField(max_length=50)),
                ('sampleSizeValue', models.FloatField()),
                ('sampleSizeUnit', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'CoralBleachData',
            },
        ),
        migrations.CreateModel(
            name='CoralBleachDataField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100)),
                ('field_type', models.CharField(max_length=100)),
                ('title_zh_tw', models.CharField(max_length=255)),
                ('title_en', models.CharField(max_length=255)),
                ('content_zh_tw', models.TextField(blank=True, null=True)),
                ('content_en', models.TextField(blank=True, null=True)),
                ('show', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'CoralBleachDataField',
            },
        ),
    ]
