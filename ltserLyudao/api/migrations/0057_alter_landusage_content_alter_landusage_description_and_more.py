# Generated by Django 4.1.1 on 2024-09-19 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0056_alter_landusage_content_alter_landusage_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landusage',
            name='content',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='landusage',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='landusage',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='social_observation__images/'),
        ),
    ]
