# Generated by Django 3.2.8 on 2021-10-24 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0004_auto_20211023_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentclass',
            name='instructor',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='studentclass',
            name='class_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
