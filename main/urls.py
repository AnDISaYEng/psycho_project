from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AnimeViewSet, GenreViewSet, EpisodeView, FavoritesListView, SeasonCreate, FavoritesCreateView, \
    FavoritesDestroyView

router = DefaultRouter()
router.register('anime', AnimeViewSet)
router.register('genre', GenreViewSet)
router.register('episode', EpisodeView)

urlpatterns = [
    path('', include(router.urls)),
    path('add_season/', SeasonCreate.as_view()),
    path('favorites/', FavoritesListView.as_view()),
    path('favorites/add/', FavoritesCreateView.as_view()),
    path('favorites/delete/<int:pk>/', FavoritesDestroyView.as_view()),
]
