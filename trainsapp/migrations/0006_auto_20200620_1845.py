# Generated by Django 3.0.5 on 2020-06-20 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trainsapp', '0005_auto_20200616_1252'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Class',
            new_name='CarriageClass',
        ),
        migrations.RenameField(
            model_name='carriage',
            old_name='Class',
            new_name='CarriageClass',
        ),
    ]
