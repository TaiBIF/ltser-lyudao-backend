# Generated by Django 4.2 on 2023-07-20 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_formlink_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formlink',
            old_name='title',
            new_name='name',
        ),
    ]
