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
        stations = helpers.GetConnectedStations(request.GET.get('from',''), request.GET.get('to',''))
        platforms = helpers.GetConnectedPlatforms(stations)
        lineplatforms = helpers.GetConnectedLinePlatforms(platforms)
        connections = helpers.GetConnectionsDataForSerializer(lineplatforms)
        serializer = serializers.ConnectionSerializer(connections, many=True)
        return Response(serializer.data)
    
@api_view(['GET', 'POST'])
def buy_ticket(request):
    if request.method == 'GET':
        if request.GET.get('from','') and request.GET.get('to',''):
            stations = helpers.GetConnectedStations(request.GET.get('from',''),    request.GET.get('to',''))
            platforms = helpers.GetConnectedPlatforms(stations)
            lineplatforms = helpers.GetConnectedLinePlatforms(platforms)
            connections = helpers.GetConnectionsDataForSerializer(lineplatforms)

            connections = helpers.AddDataForBuyer(connections)

            serializer = serializers.DataForBuyerSerializer(connections, many=True)
            return Response(serializer.data)
    if request.method == 'POST':
        pass