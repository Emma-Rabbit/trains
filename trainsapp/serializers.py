from . import models
from rest_framework import serializers

class CarriageClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarriageClass
        fields = ['Name']

class CarriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Carriage
        fields = ['Train', 'CarriageClass']

class TrainSerializer(serializers.ModelSerializer):
    # Carriages = serializers.StringRelatedField(many=True)
    Carriages = CarriageSerializer(many=True)
    class Meta:
        model = models.Train
        fields = ['id','Name', 'Carriages']

class StationSerlializer(serializers.ModelSerializer):
    class Meta:
        model = models.Station
        fields = ['id','Name']

class PlatformSerializer(serializers.ModelSerializer):
    Station = StationSerlializer()
    class Meta:
        model = models.Platform
        fields = ['id','Station', 'Name']

class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Line
        fields = ['id']

class LinePlatformSerializer(serializers.ModelSerializer):
    Platform = PlatformSerializer()
    Line = LineSerializer()
    class Meta:
        model = models.LinePlatform
        fields = ['id', 'Line', 'Platform', 'Order', 'TimeToNext', 'DistanceToNext']

class DepartureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Departure
        fields = ['id', 'Train', 'Line', 'Time']

class ConnectionSerializer(serializers.Serializer):
    start = LinePlatformSerializer(required=True)
    finish = LinePlatformSerializer(required=True)
    departure_time = serializers.TimeField(required=True)