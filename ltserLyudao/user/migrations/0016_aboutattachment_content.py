# Generated by Django 4.1.1 on 2023-08-01 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0015_about_aboutattachment"),
    ]

    operations = [
        migrations.AddField(
            model_name="aboutattachment",
            name="content",
            field=models.TextField(blank=True, null=True),
        ),
    ]
