from django.db import models
from django.contrib.auth.models import User


class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cash_in_hand = models.IntegerField()

class WatchListModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin_short = models.CharField(max_length=100)


