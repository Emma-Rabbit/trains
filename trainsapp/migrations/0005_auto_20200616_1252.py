# Generated by Django 3.0.5 on 2020-06-16 10:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainsapp', '0004_auto_20200616_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='Number',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
