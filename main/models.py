from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Anime(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.name


class Season(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='seasons')
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)

    def __str__(self):
        return f'{self.number} сезон'


class Episode(models.Model):
    name = models.CharField(max_length=50)
    number = models.PositiveIntegerField()
    preview = models.ImageField()
    video = models.FileField()
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episodes')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')

    def __str__(self):
        return f'{self.number} серия'


class Favorites(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return self.anime.name
