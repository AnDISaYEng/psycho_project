from django.db import models


class Anime(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Season(models.Model):
    number = models.PositiveIntegerField()
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='seasons')

    def __str__(self):
        return self.number


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Episode(models.Model):
    name = models.CharField(max_length=50)
    number = models.PositiveIntegerField()
    preview = models.ImageField()
    video = models.FileField()
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='episodes')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='episodes')
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return f'{self.number} серия'
