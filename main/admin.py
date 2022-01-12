from django.contrib import admin

from .models import Anime, Episode, Genre, Season, Favorites

admin.site.register(Anime)
admin.site.register(Season)
admin.site.register(Genre)
admin.site.register(Episode)
admin.site.register(Favorites)
