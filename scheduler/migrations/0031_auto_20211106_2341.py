# Generated by Django 3.2.9 on 2021-11-07 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0030_auto_20211106_2340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolistitem',
            name='users',
        ),
        migrations.AddField(
            model_name='todolistitem',
            name='users',
            field=models.ManyToManyField(to='scheduler.Profile'),
        ),
    ]