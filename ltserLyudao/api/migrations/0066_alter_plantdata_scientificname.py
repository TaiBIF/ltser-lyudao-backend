# Generated by Django 4.1.1 on 2024-09-23 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0065_alter_plantdata_dataid_alter_plantdata_eventid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantdata',
            name='scientificName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
