from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    winnings = models.IntegerField(default=0)


class Game(models.Model):
    """
        u_name - unique name of room
        status - 2 possible statuses (w - waiting, p - playing)
    """
    u_name = models.CharField(max_length=200, unique=True)
    status = models.CharField(max_length=20, default="w")
    player_1 = models.CharField(max_length=100, default=None, null=True, blank=True)
    player_2 = models.CharField(max_length=100, default=None, null=True, blank=True)
    profile_1 = models.ForeignKey(Player, models.CASCADE, related_name="first", default=None, null=True, blank=True)
    profile_2 = models.ForeignKey(Player, models.CASCADE, related_name="second", default=None, null=True, blank=True)
    turn = models.CharField(max_length=100, default=None, null=True, blank=True)
    chart = models.CharField(max_length=9, default=".........")

    def __str__(self):
        return self.u_name


