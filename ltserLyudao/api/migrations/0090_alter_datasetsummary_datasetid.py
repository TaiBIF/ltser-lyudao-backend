# Generated by Django 4.1.1 on 2025-03-21 05:17

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0089_alter_datasetsummary_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetsummary',
            name='datasetID',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
