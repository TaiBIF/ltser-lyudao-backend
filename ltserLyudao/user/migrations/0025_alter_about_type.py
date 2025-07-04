# Generated by Django 4.1.1 on 2023-12-22 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0024_alter_about_content_en"),
    ]

    operations = [
        migrations.AlterField(
            model_name="about",
            name="type",
            field=models.CharField(
                choices=[
                    ("ecologicalObservation", "生態觀測"),
                    ("environmentalObservation", "環境觀測"),
                    ("socialObservation", "社會觀測"),
                    ("projectIntroduction", "計畫介紹"),
                ],
                max_length=200,
            ),
        ),
    ]
