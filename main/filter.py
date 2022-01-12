from django_filters import rest_framework as filters

from .models import Anime


class AnimeFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    number_count_from_high = filters.NumberFilter(field_name='episodes.number', lookup_expr='gte')
    number_count_to_high = filters.NumberFilter(field_name='episodes.number', lookup_expr='lte')

    class Meta:
        model = Anime
        fields = ['genre']

