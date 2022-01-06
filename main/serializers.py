from rest_framework import serializers

from .models import Anime, Genre, Episode, Season, Favorites


class AnimeSerializer(serializers.ModelSerializer):
    # season = serializers.CharField(source='season.__str__()')

    class Meta:
        model = Anime
        fields = ['name', 'seasons', 'genre']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['number', 'anime', 'episodes']


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'  # ['name', 'number', 'preview', 'video', 'anime', 'season']


class FavoritesListSerializer(serializers.Serializer):
    def validate(self, attrs):
        user = self.context.get('request').user
        favorites_queryset = Favorites.objects.filter(user=user)
        # favorites_queryset = [favorites_queryset[i] for i in range(len(favorites_queryset))]
        favorites = [str(favorites_queryset[i]) for i in range(len(favorites_queryset))]
        attrs['user'] = favorites
        return attrs


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['all']


class ReviewSerializer(serializers.Serializer):
    pass
