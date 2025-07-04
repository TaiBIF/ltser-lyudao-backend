# Generated by Django 4.1.1 on 2024-09-19 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0058_oceanusage'),
    ]

    operations = [
        migrations.CreateModel(
            name='TemporalVariation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='social_observation__images/')),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('content', models.TextField(blank=True, default=None, null=True)),
            ],
            options={
                'db_table': 'temporal_variation',
            },
        ),
    ]
