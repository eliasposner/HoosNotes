# Generated by Django 3.2.8 on 2021-11-06 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0025_notefile_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notefile',
            old_name='note',
            new_name='file',
        ),
    ]
