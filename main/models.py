from django.db import models


# Create your models here.
class Bus(models.Model):
    name = models.CharField(max_length=128)
    # brand = models.CharField(max_length=128)
    people_capacity = models.IntegerField()
    characteristics = models.TextField()
    release_date = models.DateTimeField()

    def __str__(self):
        return self.name


class LongRouteName(models.Model):
    route_name = models.CharField(max_length=64)
    bus_stop_name = models.CharField(max_length=128)
    bs_num = models.IntegerField()
    bs_num_reverse = models.BooleanField()

    def __str__(self):
        if not self.bs_num_reverse:
            return f'{self.route_name} - ОСТ № {self.bs_num} - {self.bus_stop_name}'
        else:
            return f'{self.route_name} - обр. ОСТ № {self.bs_num} - {self.bus_stop_name}'


class Route(models.Model):
    bus_num = models.CharField(max_length=16)
    short_route_name = models.TextField()
    long_route = models.ManyToManyField(LongRouteName, related_name='long_route_name')
    long_route_reverse = models.ManyToManyField(LongRouteName, related_name='long_route_name_reverse')
    bus = models.ManyToManyField(Bus, related_name='buses')
    city = models.CharField(max_length=128)

    def __str__(self):
        return self.bus_num



