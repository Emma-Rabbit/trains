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
    Train = models.ForeignKey(Train,related_name='Carriages', on_delete=models.CASCADE)
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

class TrainLine(models.Model):
    Train = models.ForeignKey(Train, on_delete=models.CASCADE)
    Line = models.ForeignKey(Line, on_delete=models.CASCADE)
    def __str__(self):
        return '{} {} {}'.format(self.id, self.Train, self.Line)

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
    # SeatPos = models.ForeignKey(SeatPos, on_delete=models.CASCADE)
    # Number = models.CharField(max_length=3)
    Number = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    def __str__(self):
        return '{} {} {} {}'.format(self.id, self.Carriage, self.Number)

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
    Destination = models.ForeignKey(Platform, on_delete=models.CASCADE, related_name='dest')
    StartPlatform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    Departure = models.ForeignKey(Departure, on_delete=models.CASCADE)
    Date = models.DateField()
    def __str__(self):
        return '{} {} {} {} {}'.format(self.id, self.Platform, self.Destination, self.Departure, self.Departure)

class Reservation(models.Model):
    Ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    Discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    Seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    Price = models.IntegerField()
    def __str__(self):
        return '{} {}'.format(self.Ticket, self.Seat, self.Price)