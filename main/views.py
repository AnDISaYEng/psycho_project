from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Anime, Genre, Episode, Favorites, Season
from .permissions import IsAdmin
from .serializers import AnimeSerializer, SeasonSerializer, EpisodeSerializer, GenreSerializer, FavoritesSerializer, \
    FavoritesListSerializer


class AnimeViewSet(ModelViewSet):
    # Добавить/удалить/просмотреть_список аниме
    # Фильтрация
    # action: список серий с видео и сезонами
    # action: LikedMixin
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer

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
        serializer = EpisodeSerializer(episodes, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'list':
            return []
        return [IsAdmin()]


class SeasonCreate(CreateAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    permission_classes = [IsAdmin]


class GenreViewSet(ModelViewSet):
    # Добавить/удалить/просмотреть_список жанров
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.action == 'list':
            return []
        return [IsAdmin()]


class EpisodeView(CreateModelMixin, DestroyModelMixin, GenericViewSet):
    # Добавить/удалить/просмотреть_список(action) серий к аниме
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    permission_classes = [IsAdmin]


class ReviewViewSet(ModelViewSet):
    # Добавить/удалить/просмотреть_список(action) отзыв(-ов) к аниме
    pass


class FavoritesListView(ListAPIView):
    queryset = Favorites.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FavoritesListSerializer

    def get(self, request):
        data = request.data
        serializer = FavoritesListSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class FavoritesCreateView(CreateAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer


class FavoritesDestroyView(DestroyAPIView):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer
