# Generated by Django 3.2.7 on 2021-11-01 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0022_alter_studentclass_days'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentclass',
            old_name='days',
            new_name='days_of_the_week',
        ),
    ]
