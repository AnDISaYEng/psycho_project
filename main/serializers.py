from django.contrib.auth import get_user_model
from rest_framework import serializers

from . import likes_services
from .models import Anime, Genre, Episode, Season, Favorites, Review

User = get_user_model()


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = ['name', 'seasons', 'genre', 'slug']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('slug')
        representation['rating_count'] = instance.comments.all().count()
        representation['rating_average'] = ReviewSerializer(instance.comments.all(), many=True).data
        try:
            fl = 0
            for ordered_dict in representation['rating_average']:
                fl += ordered_dict.get('rating')
            representation['rating_average'] = fl/instance.comments.all().count()
            return representation
        except ZeroDivisionError:
            return representation


class FanSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name', 'slug']


class EpisodeSerializer(serializers.ModelSerializer):
    is_like = serializers.SerializerMethodField()

    class Meta:
        model = Episode
        fields = ['anime', 'season', 'number', 'name', 'preview', 'video', 'is_like', ]

    def get_is_like(self, post):
        user = self.context.get('request').user
        return likes_services.is_like(post, user)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes_count'] = likes_services.get_likes_user(instance).count()
        return representation


class EpisodeToNewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['was_published_recently', 'string_for_new']


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


class ReviewSerializer(serializers.ModelSerializer):
    # text = serializers.CharField(max_length=350)
    # rating = serializers.IntegerField(required=True)
    # anime = serializers.CharField(max_length=50, required=True)
    class Meta:
        model = Review
        fields = ['text', 'rating', 'anime']

    def validate_rating(self, rating):
        if rating not in [1, 2, 3, 4, 5]:
            raise serializers.ValidationError('Рейтинг может быть только от одного до пяти')
        return rating

    def validate(self, attrs):
        author = self.context.get('request').user
        anime = attrs.get('anime')
        try:
            rating = Review.objects.filter(author=author)[0]
            reviews = Review.objects.filter(anime=anime)
            if rating in reviews:
                raise serializers.ValidationError('Вы уже оставили отзыв')
            return attrs
        except IndexError:
            return attrs

    def create(self, validated_data):
        validated_data['author'] = self.context.get('request').user
        return super().create(validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class TestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email
