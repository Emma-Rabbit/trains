from . import models
from datetime import time, timedelta, datetime

def GetDepartureTime(line, order):
    lineplatforms = models.LinePlatform.objects.filter(Line=models.Line.objects.get(pk=line), Order__lt=order)
    time = 0
    for lineplat in lineplatforms:
        time += lineplat.TimeToNext
    departure = models.Departure.objects.get(Line=models.Line.objects.get(pk=line))
    print(type(departure.Time))
    departure_time = (datetime.combine(datetime.today(),departure.Time) + timedelta(minutes=time)).time()
    return departure_time