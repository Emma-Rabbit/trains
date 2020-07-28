from . import models
from datetime import time, timedelta, datetime
from math import sqrt

def GetDepartureTime(line, order):
    lineplatforms = models.LinePlatform.objects.filter(Line=models.Line.objects.get(pk=line), Order__lt=order)
    time = 0
    for lineplat in lineplatforms:
        time += lineplat.TimeToNext
    departure = models.Departure.objects.get(Line=models.Line.objects.get(pk=line))
    departure_time = (datetime.combine(datetime.today(),departure.Time) + timedelta(minutes=time)).time()
    return departure_time

def GetStationFromName(name):
    return models.Station.objects.get(Name=name)

def GetConnectedStations(from_station, to_station):
    start_s = GetStationFromName(from_station)
    finish_s = GetStationFromName(to_station)
    print('STATIONS: START ',start_s,'FINISH',finish_s)
    return {'start_s': start_s, 'finish_s': finish_s}

def GetPlatformsFromStation(station):
    return models.Platform.objects.filter(Station=station)

def GetConnectedPlatforms(stations):
    start_p = GetPlatformsFromStation(stations.get('start_s'))
    finish_p = GetPlatformsFromStation(stations.get('finish_s'))
    print('PLATFORMS: START ',start_p,'FINISH',finish_p)
    return {'start_p': start_p, 'finish_p': finish_p}

def GetConnectedLinePlatforms(platforms):
    start_lp = models.LinePlatform.objects.filter(Platform__in=platforms.get('start_p'))
    finish_lp = models.LinePlatform.objects.filter(Platform__in=platforms.get('finish_p'))
    return {'start_lp': start_lp, 'finish_lp': finish_lp}

def GetConnectionsDataForSerializer(lineplatforms):
    from_lineplatforms = lineplatforms.get('start_lp')
    to_lineplatforms = lineplatforms.get('finish_lp')
    connections = []
    for from_lineplatform in from_lineplatforms:
        for to_lineplatform in to_lineplatforms:
            if from_lineplatform.Line_id == to_lineplatform.Line_id and from_lineplatform.Order < to_lineplatform.Order:
                departure = models.Departure.objects.get(Line_id=from_lineplatform.Line_id)
                connections.append({
                    'line' : models.Line.objects.get(pk=from_lineplatform.Line_id),
                    'train' : models.Train.objects.get(pk=departure.Train.id),
                    'departure': departure,
                    'start': from_lineplatform, 
                    'finish': to_lineplatform,
                    'departure_time': GetDepartureTime(from_lineplatform.Line_id,from_lineplatform.Order),
                    'arrival_time': GetDepartureTime(to_lineplatform.Line_id,to_lineplatform.Order),
                })
    return connections

def AddDataForBuyer(connections, date):
    for connection in connections:
        carriages = models.Carriage.objects.filter(Train=connection['train'])
        connection['carriages'] = carriages
        seats = models.Seat.objects.filter(Carriage__in=carriages)
        seats_dict = {}
        for seat in seats:
            s = {"Carriage" : seat.Carriage,"Number" : seat.Number}
            seats_dict[seat.id] = s
        connection['seats'] = seats_dict
    # print('CONNECTIONS 3: ',connections)
    connections = GetTakenSeats(connections, date)
    # print('CONNECTIONS 4: ',connections)
    return connections

def CalculateReservationPrice(start, finish, discountid):
    start = models.LinePlatform.objects.get(pk=start)
    finish = models.LinePlatform.objects.get(pk=finish)
    lineplatforms = models.LinePlatform.objects.filter(Line=start.Line, Order__gte=start.Order).filter(Order__lt=finish.Order)
    distance = 0
    for lp in lineplatforms:
        distance += lp.DistanceToNext
    discount = models.Discount.objects.get(pk=discountid).Percentage
    price = sqrt(distance)*discount/100
    return round(price, 2)

def GetTakenSeats(connections, date):
    for connection in connections:
        date = datetime.strptime(date,'%Y-%m-%d')
        # print('-------------DATA:',date, type(date))
        tickets = models.Ticket.objects.filter(
            Day=date,
            StartPlatform__Order__lt=connection['finish'].Order,
            Destination__Order__gt=connection['start'].Order)
        print('CONNECTION START, FINISH: ',connection['start'].Order, connection['finish'].Order)
        # print('TICKETS: ', tickets)
        reservations = models.Reservation.objects.filter(Ticket__in=tickets)
        # print('RESERVATIONS: ',reservations)
        for seat in connection['seats']:
            connection['seats'][seat]['Taken'] = False
        for res in reservations:
            print('SEAT TAKEN = TRUE', res.Seat_id)
            seat = connection['seats'][res.Seat_id]['Taken'] = True
    return connections