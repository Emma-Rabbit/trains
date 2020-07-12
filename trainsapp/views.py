from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from . import helpers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class TrainViewSet(viewsets.ModelViewSet):
    queryset = models.Train.objects.all()
    serializer_class = serializers.TrainSerializer

class CarriageViewSet(viewsets.ModelViewSet):
    queryset = models.Carriage.objects.all()
    serializer_class = serializers.CarriageSerializer

@api_view(['GET','POST'])
def carriage_list(request):
    if request.method == 'GET':
        carraiges = models.Carriage.objects.all()
        serializer = serializers.CarriageSerializer(carraiges, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = serializers.CarriageSerializer(data=request.data)
        if serializer.is_valid():
            newCarriage = serializer.save()
            print(newCarriage)
            for seat in range(1,101):
                s = models.Seat(Carriage=models.Carriage.objects.get(pk=newCarriage.id), Number=seat)
                s.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def lineplatform_list(request):
    if request.method == 'GET':
        lineplatforms = models.LinePlatform.objects.all()
        serializer = serializers.LinePlatformSerializer(lineplatforms, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = serializers.LinePlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def connection_list(request):
    if request.GET.get('from','') and request.GET.get('to',''):
        from_station = models.Station.objects.get(Name=request.GET.get('from',''))
        to_station = models.Station.objects.get(Name=request.GET.get('to',''))
        print('STATIONS: ', from_station, to_station)

        from_platforms = models.Platform.objects.filter(Station=from_station)
        to_platforms = models.Platform.objects.filter(Station=to_station)
        print("PLATFORMS: ", from_platforms, to_platforms)

        from_lineplatforms = models.LinePlatform.objects.filter(Platform__in=from_platforms)
        to_lineplatforms = models.LinePlatform.objects.filter(Platform__in=to_platforms)
        print("LINEPLATFORMS: ", from_lineplatforms, to_lineplatforms)

        lines = []
        for from_lineplatform in from_lineplatforms:
            for to_lineplatform in to_lineplatforms:
                if from_lineplatform.Line_id == to_lineplatform.Line_id and from_lineplatform.Order < to_lineplatform.Order:
                    departure = models.Departure.objects.get(Line_id=from_lineplatform.Line_id)
                    lines.append({
                        'start': from_lineplatform, 
                        'finish': to_lineplatform,
                        'departure_time': helpers.GetDepartureTime(from_lineplatform.Line_id,from_lineplatform.Order),
                    })
        print(lines)
        serializer = serializers.ConnectionSerializer(lines, many=True)
        return Response(serializer.data)
    