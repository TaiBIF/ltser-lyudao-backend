# Generated by Django 4.1.1 on 2024-12-05 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0079_alter_weatherdata_par'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weatherdata',
            name='RH',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='airTemperature',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='gustSpeed',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='precipitation',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='pressure',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='solarRadiation',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='windDirection',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='weatherdata',
            name='windSpeed',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
