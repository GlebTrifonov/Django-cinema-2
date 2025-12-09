from django.contrib import admin
from .models import Film, FavoriteFilm, CinemaHall, MovieSession

# Register your models here.
admin.site.register(Film)
admin.site.register(FavoriteFilm)
admin.site.register(CinemaHall)
admin.site.register(MovieSession)