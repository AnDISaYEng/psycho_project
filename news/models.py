from django.db import models

from main.models import Anime


class Post(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.RESTRICT, related_name='posts')
    title = models.CharField(max_length=150)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title
