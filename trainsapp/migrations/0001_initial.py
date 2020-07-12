# Generated by Django 3.0.5 on 2020-05-28 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carriage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Departure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Percentage', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='SeatPos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TrainLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LineId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Line')),
                ('TrainId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Train')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.DateField()),
                ('DepartureId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Departure')),
                ('DestinationId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dest', to='trainsapp.Platform')),
                ('PlatformId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Platform')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.CharField(max_length=3)),
                ('CarriageId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Carriage')),
                ('SeatPosId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.SeatPos')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Price', models.IntegerField()),
                ('DiscountId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Discount')),
                ('SeatId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Seat')),
                ('TicketId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Ticket')),
            ],
        ),
        migrations.AddField(
            model_name='platform',
            name='StationId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Station'),
        ),
        migrations.CreateModel(
            name='LinePlatform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order', models.IntegerField()),
                ('TimeToNext', models.IntegerField()),
                ('DistanceToNext', models.IntegerField()),
                ('LineId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Line')),
                ('PlatformId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Platform')),
            ],
        ),
        migrations.AddField(
            model_name='departure',
            name='LineId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Line'),
        ),
        migrations.AddField(
            model_name='departure',
            name='TrainId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Train'),
        ),
        migrations.AddField(
            model_name='carriage',
            name='ClassId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Class'),
        ),
        migrations.AddField(
            model_name='carriage',
            name='TrainId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainsapp.Train'),
        ),
    ]
