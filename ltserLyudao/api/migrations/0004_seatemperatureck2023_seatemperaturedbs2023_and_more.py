# Generated by Django 4.2 on 2023-06-23 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_weatherdata_rh_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeaTemperatureCK2023',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataID', models.CharField(max_length=255)),
                ('eventID', models.CharField(max_length=255)),
                ('resourceName', models.CharField(max_length=255)),
                ('locationID', models.CharField(max_length=255)),
                ('verbatimDepth', models.CharField(max_length=255)),
                ('fieldNumber', models.IntegerField(null=True)),
                ('measurementDeterminedDate', models.DateTimeField()),
                ('seaTemperature', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'SeaTemperatureCK2023',
            },
        ),
        migrations.CreateModel(
            name='SeaTemperatureDBS2023',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataID', models.CharField(max_length=255)),
                ('eventID', models.CharField(max_length=255)),
                ('resourceName', models.CharField(max_length=255)),
                ('locationID', models.CharField(max_length=255)),
                ('verbatimDepth', models.CharField(max_length=255)),
                ('fieldNumber', models.IntegerField(null=True)),
                ('measurementDeterminedDate', models.DateTimeField()),
                ('seaTemperature', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'SeaTemperatureDBS2023',
            },
        ),
        migrations.CreateModel(
            name='SeaTemperatureGG2023',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataID', models.CharField(max_length=255)),
                ('eventID', models.CharField(max_length=255)),
                ('resourceName', models.CharField(max_length=255)),
                ('locationID', models.CharField(max_length=255)),
                ('verbatimDepth', models.CharField(max_length=255)),
                ('fieldNumber', models.IntegerField(null=True)),
                ('measurementDeterminedDate', models.DateTimeField()),
                ('seaTemperature', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'SeaTemperatureGG2023',
            },
        ),
        migrations.CreateModel(
            name='SeaTemperatureGW2023',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataID', models.CharField(max_length=255)),
                ('eventID', models.CharField(max_length=255)),
                ('resourceName', models.CharField(max_length=255)),
                ('locationID', models.CharField(max_length=255)),
                ('verbatimDepth', models.CharField(max_length=255)),
                ('fieldNumber', models.IntegerField(null=True)),
                ('measurementDeterminedDate', models.DateTimeField()),
                ('seaTemperature', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'SeaTemperatureGW2023',
            },
        ),
        migrations.CreateModel(
            name='SeaTemperatureNL2023',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataID', models.CharField(max_length=255)),
                ('eventID', models.CharField(max_length=255)),
                ('resourceName', models.CharField(max_length=255)),
                ('locationID', models.CharField(max_length=255)),
                ('verbatimDepth', models.CharField(max_length=255)),
                ('fieldNumber', models.IntegerField(null=True)),
                ('measurementDeterminedDate', models.DateTimeField()),
                ('seaTemperature', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'SeaTemperatureNL2023',
            },
        ),
        migrations.CreateModel(
            name='SeaTemperatureSL2023',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataID', models.CharField(max_length=255)),
                ('eventID', models.CharField(max_length=255)),
                ('resourceName', models.CharField(max_length=255)),
                ('locationID', models.CharField(max_length=255)),
                ('verbatimDepth', models.CharField(max_length=255)),
                ('fieldNumber', models.IntegerField(null=True)),
                ('measurementDeterminedDate', models.DateTimeField()),
                ('seaTemperature', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'SeaTemperatureSL2023',
            },
        ),
        migrations.CreateModel(
            name='SeaTemperatureWQG2023',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataID', models.CharField(max_length=255)),
                ('eventID', models.CharField(max_length=255)),
                ('resourceName', models.CharField(max_length=255)),
                ('locationID', models.CharField(max_length=255)),
                ('verbatimDepth', models.CharField(max_length=255)),
                ('fieldNumber', models.IntegerField(null=True)),
                ('measurementDeterminedDate', models.DateTimeField()),
                ('seaTemperature', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'SeaTemperatureWQG2023',
            },
        ),
        migrations.CreateModel(
            name='SeaTemperatureYZH2023',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataID', models.CharField(max_length=255)),
                ('eventID', models.CharField(max_length=255)),
                ('resourceName', models.CharField(max_length=255)),
                ('locationID', models.CharField(max_length=255)),
                ('verbatimDepth', models.CharField(max_length=255)),
                ('fieldNumber', models.IntegerField(null=True)),
                ('measurementDeterminedDate', models.DateTimeField()),
                ('seaTemperature', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'SeaTemperatureYZH2023',
            },
        ),
        migrations.CreateModel(
            name='SeaTemperatureZP2023',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataID', models.CharField(max_length=255)),
                ('eventID', models.CharField(max_length=255)),
                ('resourceName', models.CharField(max_length=255)),
                ('locationID', models.CharField(max_length=255)),
                ('verbatimDepth', models.CharField(max_length=255)),
                ('fieldNumber', models.IntegerField(null=True)),
                ('measurementDeterminedDate', models.DateTimeField()),
                ('seaTemperature', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'SeaTemperatureZP2023',
            },
        ),
    ]
