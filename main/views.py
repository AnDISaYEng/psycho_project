from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

import parser_top100
from . import likes_services
from .filter import AnimeFilter
from .models import Anime, Genre, Episode, Favorites, Season, Review
from .permissions import IsAdmin, IsAuthor, IsAuthorFavorites
from .serializers import AnimeSerializer, SeasonSerializer, EpisodeSerializer, GenreSerializer, FavoritesSerializer, \
    FavoritesListSerializer, FanSerializer, ReviewSerializer, EpisodeToNewSerializer, TopSerializer
from .tasks import send_mail_task


class LikedMixin:
    @action(['POST'], detail=True)
    def like(self, request, pk):
        anime = self.get_object()
        likes_services.add_like(anime, request.user)
        return Response()

    @action(['POST'], detail=True)
    def unlike(self, request, pk):
        anime = self.get_object()
        likes_services.remove_like(anime, request.user)
        return Response()

    @action(['GET'], detail=True)
    def likes(self, request, pk):
        anime = self.get_object()
        likes = likes_services.get_likes_user(anime)
        serializer = FanSerializer(likes, many=True)
        return Response(serializer.data)


class AnimeViewSet(ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = AnimeFilter
    search_fields = ['name']

    @action(['GET'], detail=True)
    def seasons(self, request, pk):
        anime = self.get_object()
        seasons = anime.seasons.all()
        serializer = SeasonSerializer(seasons, many=True)
        return Response(serializer.data)

    @action(['GET'], detail=True)
    def episodes(self, request, pk):
        anime = self.get_object()
        episodes = anime.episodes.all()
        serializer = EpisodeSerializer(episodes, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(['GET'], detail=True)
    def reviews(self, request, pk):
        anime = self.get_object()
        reviews = anime.comments.all()
        serializer = ReviewSerializer(reviews, context={'request': request}, many=True)
        return Response(serializer.data)

    @action(['GET'], detail=False)
    def new(self, request):
        episodes = Episode.objects.all()
        serializer = EpisodeToNewSerializer(episodes, many=True)
        new_episodes = []
        for ordered_dict in serializer.data:
            if ordered_dict.get('was_published_recently'):
                ordered_dict.pop('was_published_recently')
                new_episodes.append(ordered_dict.get('string_for_new'))
        print(new_episodes)
        return Response(new_episodes)

    def get_permissions(self):
        if self.action in ['likes', 'list', 'reviews', 'new']:
            return []
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            return [IsAdmin()]
        return [IsAuthenticated()]


class SeasonCreate(CreateAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsAdmin]


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.action == 'list':
            return []
        return [IsAdmin()]


class EpisodeView(CreateModelMixin, DestroyModelMixin, GenericViewSet, LikedMixin):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [IsAdmin]

    def get_permissions(self):
        if self.action in ['like', 'unlike']:
            return [IsAuthenticated()]
        if self.action in ['create', 'destroy']:
            return [IsAdmin()]
        return []


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAdmin()] or [IsAuthor()]
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAdmin()]


class FavoritesViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = Favorites.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritesListSerializer

    def list(self, request):
        user = request.user
        favorites = Favorites.objects.filter(user=user)
        serializer = FavoritesListSerializer(favorites, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        serializer = FavoritesSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.create()
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [IsAuthenticated()]
        return [IsAuthorFavorites()]


class SendMailView(ListAPIView):
    permission_classes = [IsAdmin]

    def list(self, request):
        users_queryset = get_user_model().objects.all()
        users = [str(i) for i in users_queryset]
        send_mail_task.delay(users)
        return Response('?????????????????? ????????????????????')


class TopView(ListAPIView):
    def get(self, request):
        return Response(parser_top100.main())
