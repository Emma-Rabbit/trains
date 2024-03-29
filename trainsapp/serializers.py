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

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seat
        fields = ['id','Carriage', 'Number']

class FormattedSeatSerializer(serializers.Serializer):
    Carriage = CarriageSerializer()
    Number = serializers.IntegerField()
    Taken = serializers.BooleanField()

class ConnectionSerializer(serializers.Serializer):
    start = LinePlatformSerializer(required=True)
    finish = LinePlatformSerializer(required=True)
    departure_time = serializers.TimeField(required=True)
    arrival_time = serializers.TimeField(required=True)

class DataForBuyerSerializer(serializers.Serializer):
    start = LinePlatformSerializer(required=True)
    finish = LinePlatformSerializer(required=True)
    departure_time = serializers.TimeField(required=True)
    arrival_time = serializers.TimeField(required=True)
    carriages = CarriageSerializer(many=True)
    seats = serializers.DictField(
        child = FormattedSeatSerializer()
    )

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reservation
        fields = ['id', 'Ticket', 'Discount', 'Seat', 'Price']

class TicketSerializer(serializers.ModelSerializer):
    Day = serializers.DateField(input_formats=['%Y-%m-%d'])
    class Meta:
        model = models.Ticket
        fields = ['id','Destination','StartPlatform', 'Departure', 'Day']    
    def create(self, validated_data):
        print("DATA IN TICKET SERIALIZER: ",validated_data)
        return super().create(validated_data)