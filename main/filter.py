from django_filters import rest_framework as filters

from .models import Anime


class AnimeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Anime
        fields = ['genre']

