from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Anime, Genre, Episode, Season, Favorites

User = get_user_model()

class AnimeSerializer(serializers.ModelSerializer):
    # genre = serializers.CharField(source='genre.name')

    class Meta:
        model = Anime
        fields = ['name', 'seasons', 'genre', 'slug']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('slug')
        return representation


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'  # ['name', 'number', 'preview', 'video', 'anime', 'season']


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['anime', 'number', 'name', 'slug']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['episodes'] = EpisodeSerializer(instance.episodes.all(), many=True).data
        representation.pop('slug')
        return representation


class FavoritesListSerializer(serializers.Serializer):
    user = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate(self, attrs):
        user = attrs.get('user')
        favorites_queryset = Favorites.objects.filter(user=user)
        favorites_queryset = [favorites_queryset[i] for i in range(len(favorites_queryset))]
        favorites = [str(favorites_queryset[i]) for i in range(len(favorites_queryset))]
        attrs['user'] = favorites
        return attrs


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate_anime(self, anime):
        if not Anime.objects.filter(name=anime).exists():
            raise serializers.ValidationError('Такого поста не существует')
        return anime

    def validate(self, attrs):
        user = attrs.get('user')
        anime = attrs.get('anime')
        favorites_queryset = Favorites.objects.filter(user=user)
        favorites_queryset = [favorites_queryset[i] for i in range(len(favorites_queryset))]
        favorites = [str(favorites_queryset[i]) for i in range(len(favorites_queryset))]
        if str(anime) in favorites:
            raise serializers.ValidationError('Вы уже добавили anime в избранное')
        return attrs

    def create(self, validated_data):
        return super().create(validated_data)


class ReviewSerializer(serializers.Serializer):
    pass
