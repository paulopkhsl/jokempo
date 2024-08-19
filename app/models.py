from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    player_choice = models.CharField(max_length=10)
    computer_choice = models.CharField(max_length=10)
    result = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

class Ranking(models.Model):
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    class Meta:
        ordering = ['-score']