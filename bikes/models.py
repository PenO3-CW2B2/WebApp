from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Bike(models.Model):
    secret = models.CharField(max_length=32)
    modified_date = models.DateTimeField(auto_now=True)
    battery = models.PositiveSmallIntegerField(default=32767)
    last_longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    last_laltitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    owners = models.ManyToManyField(User, blank=True)


class Contract(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    time_start = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(default=None, null=True)
    payed = models.BooleanField(default=False)
