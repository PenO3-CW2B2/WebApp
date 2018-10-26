from django.db import models
from django.conf import settings

# Create your models here.

class bikes(models.Model):
    secret = models.CharField(max_length=32)
    modified_date = models.DateTimeField(auto_now=True)
    battery = models.PositiveSmallIntegerField()
    last_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    last_laltitude = models.DecimalField(max_digits=9, decimal_places=6)

class contracts(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_start = models.DateTimeField(auto_now_add=True)
    time_end = models.DateTimeField(default=None)
    payed = models.BooleanField(default=False)
