from django.db import models


class Game(models.Model):
    """
        u_name - unique name of room
        status - 3 possible statuses (w - waiting, p - playing)
    """
    u_name = models.CharField(max_length=200, unique=True)
    status = models.CharField(max_length=20, default="w")
    player_1 = models.CharField(max_length=100, default=None, null=True, blank=True)
    player_2 = models.CharField(max_length=100, default=None, null=True, blank=True)
    turn = models.CharField(max_length=100, default=None, null=True, blank=True)
    chart = models.CharField(max_length=9, default=".........")

    def __str__(self):
        return self.u_name
