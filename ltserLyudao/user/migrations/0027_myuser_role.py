# Generated by Django 4.1.1 on 2023-12-26 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0026_alter_about_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="myuser",
            name="role",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
