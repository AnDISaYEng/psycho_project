import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='anime_likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


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
    likes = GenericRelation(Like)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.anime}: {self.number} серия'

    @property
    def was_published_recently(self):
        return self.created_at >= timezone.now() - datetime.timedelta(days=1)


class Favorites(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return self.anime.name


class Review(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=350)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f'{self.author}: {self.rating}'
