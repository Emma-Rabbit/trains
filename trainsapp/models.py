from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Train(models.Model):
    Name = models.CharField(max_length=10)
    def __str__(self):
        return '{} {}'.format(self.id, self.Name)

class CarriageClass(models.Model):
    Name = models.CharField(max_length=1)
    def __str__(self):
        return 'class: {}'.format(self.Name)

class Carriage(models.Model):
    Train = models.ForeignKey(Train, on_delete=models.CASCADE) # usunęłam tu takie coś related_name='Carriages' idk co to xd
    CarriageClass = models.ForeignKey(CarriageClass, on_delete=models.CASCADE)
    def __str__(self):
        return 'id : {}, train: {}, {}'.format(self.id, self.Train, self.CarriageClass)

class Station(models.Model):
    Name = models.CharField(max_length=50)
    def __str__(self):
        return '{} {}'.format(self.id, self.Name)

class Line(models.Model):
    def __str__(self):
        return '{}'.format(self.id)

class Platform(models.Model):
    Station = models.ForeignKey(Station, on_delete=models.CASCADE)
    Name = models.CharField(max_length=1)
    def __str__(self):
        return '{}, station {}, name {}'.format(self.id, self.Station, self.Name)

# class SeatPos(models.Model):
#     Name = models.CharField(max_length=1)
#     def __str__(self):
#         return '{}'.format(self.Name)

# class Compartment(models.Model):
#     Carriage = models.ForeignKey(Carriage, on_delete=models.CASCADE)
#     def __str__(self):
#         return '{}, {}'.format(self.id, self.Carriage)

class Seat(models.Model):
    Carriage = models.ForeignKey(Carriage, on_delete=models.CASCADE)
    Number = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    def __str__(self):
        return '{} {} {}'.format(self.id, self.Carriage, self.Number)

# class TakenSeat(models.Model):
#     Seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
#     FromLineplatform = models.ForeignKey(LinePlatform, on_delete=models.CASCADE)
#     ToLineplatform = models.ForeignKey(LinePlatform, on_delete=models.CASCADE)
#     Departure = models.ForeignKey(Departure, on_delete=models.CASCADE)

class LinePlatform(models.Model):
    Platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    Line = models.ForeignKey(Line, on_delete=models.CASCADE)
    Order = models.IntegerField()
    TimeToNext = models.IntegerField()
    DistanceToNext = models.IntegerField()
    def __str__(self):
        return 'id: {}, Platform: {}, Line: {}, Order: {}'.format(self.id, self.Platform, self.Line, self.Order)

class Departure(models.Model):
    Train = models.ForeignKey(Train, on_delete=models.CASCADE)
    Line = models.ForeignKey(Line, on_delete=models.CASCADE)
    Time = models.TimeField()
    def __str__(self):
        return '{} {} {}'.format(self.id, self.Train, self.Time)

class Discount(models.Model):
    Name = models.CharField(max_length=50)
    Percentage = models.IntegerField()
    def __str__(self):
        return '{} {}'.format(self.Name, self.Percentage)

class Ticket(models.Model):
    Destination = models.ForeignKey(LinePlatform, on_delete=models.CASCADE, related_name='dest')
    StartPlatform = models.ForeignKey(LinePlatform, on_delete=models.CASCADE)
    Departure = models.ForeignKey(Departure, on_delete=models.CASCADE)
    Day = models.DateField()
    def __str__(self):
        return '{} {} {} {} {}'.format(self.id, self.StartPlatform, self.Destination, self.Departure, self.Day)

class Reservation(models.Model):
    Ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    Discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    Seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    Price = models.FloatField()
    def __str__(self):
        return '{} {}'.format(self.Ticket, self.Seat, self.Price)