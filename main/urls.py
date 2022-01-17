from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AnimeViewSet, GenreViewSet, EpisodeView, FavoritesViewSet, SeasonCreate, \
    ReviewViewSet, SendMailView

router = DefaultRouter()
router.register('anime', AnimeViewSet)
router.register('genre', GenreViewSet)
router.register('episode', EpisodeView)
router.register('review', ReviewViewSet)
router.register('favorites', FavoritesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('add_season/', SeasonCreate.as_view()),
    path('send_mail/', SendMailView.as_view()),
]
