from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet


class AnimeViewSet(ModelViewSet):
    # Добавить/удалить/просмотреть_список аниме
    # Фильтрация
    # action: список серий с видео и сезонами
    # action: LikedMixin
    pass


class GenreViewSet(ModelViewSet):
    # Добавить/удалить/просмотреть_список жанров
    pass


class EpisodeViewSet(ModelViewSet):
    # Добавить/удалить/просмотреть_список(action) серий к аниме
    pass


class ReviewViewSet(ModelViewSet):
    # Добавить/удалить/просмотреть_список(action) отзыв(-ов) к аниме
    pass


class FavoritesView(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    pass
