from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from . import helpers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

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
            for seat in range(1,11):
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
        if request.GET.get('from','') and request.GET.get('to','') and request.GET.get('date',''):
            stations = helpers.GetConnectedStations(request.GET.get('from',''),request.GET.get('to',''))
            platforms = helpers.GetConnectedPlatforms(stations)
            lineplatforms = helpers.GetConnectedLinePlatforms(platforms)
            connections = helpers.GetConnectionsDataForSerializer(lineplatforms)
            # print('CONNECTIONS: ',connections)
            connections = helpers.AddDataForBuyer(connections,request.GET.get('date',''))
            # print('CONNECTIONS: ',connections)
            serializer = serializers.DataForBuyerSerializer(connections, many=True)
            return Response(serializer.data)
    if request.method == 'POST':
        print('POST REQUEST: ',request.data)
        print('request.data destid: ',request.data['destination_id'])
        ticket_data = {
            'Destination' : request.data['destination_id'],
            'StartPlatform' : request.data['startplatform_id'],
            'Departure' : request.data['departure_id'],
            'Day' : request.data['day']
            }
        ticket_serializer = serializers.TicketSerializer(data=ticket_data)
        if not ticket_serializer.is_valid():
            return Response(ticket_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        new_ticket = ticket_serializer.save()
        reservations_data = []
        new_res =[]
        isvalid = True
        for reservation in request.data['reservations']:
            price = helpers.CalculateReservationPrice(ticket_data['StartPlatform'],ticket_data['Destination'], reservation['discount_id'])
            new_reservation = {
                'Seat': reservation['seat_id'],
                'Discount' : reservation['discount_id'],
                'Ticket' : new_ticket.id,
                'Price' : price
                }
            reser_serializer = serializers.ReservationSerializer(data=new_reservation)
            if reser_serializer.is_valid():
                new_res.append(reser_serializer)
            else:
                isvalid = False
        if not isvalid:
            new_ticket.delete()
            return Response(reser_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        for res in new_res:
            res.save()
        return Response(status=status.HTTP_201_CREATED)