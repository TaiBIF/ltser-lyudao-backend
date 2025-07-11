# Generated by Django 4.2 on 2023-07-01 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_fishdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZoobenthosData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataID', models.CharField(max_length=100)),
                ('eventID', models.CharField(max_length=100)),
                ('eventDate', models.DateField()),
                ('season', models.CharField(max_length=50)),
                ('day_or_night', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('river', models.CharField(max_length=100)),
                ('locationID', models.CharField(max_length=10)),
                ('surveyObjectID', models.CharField(max_length=10)),
                ('surveyObject', models.CharField(max_length=100)),
                ('phylum', models.CharField(max_length=100)),
                ('phylum_c', models.CharField(max_length=100)),
                ('class_name', models.CharField(max_length=100)),
                ('class_c', models.CharField(max_length=100)),
                ('family', models.CharField(max_length=100)),
                ('family_c', models.CharField(max_length=100)),
                ('scientificName', models.CharField(max_length=100)),
                ('vernacularName', models.CharField(max_length=100)),
                ('taxonRank', models.CharField(max_length=50)),
                ('individualCount', models.IntegerField()),
                ('samplingProtocol', models.CharField(max_length=100)),
                ('habitat', models.CharField(max_length=100)),
                ('informationWithheld', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'ZoobenthosData',
            },
        ),
    ]
