# Generated by Django 3.2.8 on 2021-10-31 00:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0019_auto_20211030_1955'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studentclass',
            unique_together={('class_name', 'instructor')},
        ),
    ]