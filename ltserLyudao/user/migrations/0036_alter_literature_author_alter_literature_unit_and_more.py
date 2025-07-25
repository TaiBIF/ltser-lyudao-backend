# Generated by Django 4.1.1 on 2025-07-24 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0035_rename_name_literature_title_literature_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='literature',
            name='author',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='literature',
            name='unit',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='literature',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
