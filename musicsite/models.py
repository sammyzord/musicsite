from django.db import models
from django.contrib.auth.models import User


class Song(models.Model):
    artist_name = models.CharField("artist's name", max_length=100)
    song_name = models.CharField(max_length=100)
    song_genre = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
