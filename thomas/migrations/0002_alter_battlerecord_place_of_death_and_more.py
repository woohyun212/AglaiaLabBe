# Generated by Django 5.0.7 on 2024-09-09 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thomas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='battlerecord',
            name='place_of_death',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='battlerecord',
            name='place_of_death2',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='battlerecord',
            name='place_of_death3',
            field=models.IntegerField(null=True),
        ),
    ]
