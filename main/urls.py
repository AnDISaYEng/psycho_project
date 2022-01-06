from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AnimeViewSet, GenreViewSet, EpisodeView, FavoritesView

router = DefaultRouter()
router.register('anime', AnimeViewSet)
router.register('genre', GenreViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('episodes/', EpisodeView.as_view()),
    path('favorites/', FavoritesView.as_view()),
]
