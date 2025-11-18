from rest_framework import serializers
from .models import Film, FavoriteFilm, CinemaHall, MovieSession
from django.contrib.auth.models import User


class FilmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Film
        fields = '__all__'

class FavoriteFilmSerializer(serializers.ModelSerializer):
    film_title = serializers.CharField(source='film.title', read_only=True)
    film_description = serializers.CharField(source='film.description', read_only=True)

    class Meta:
        model = FavoriteFilm
        fields = ['id', 'film', 'film_title', 'film_description', 'added_at']
        read_only_fields = ['added_at']


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = '__all__'


class MovieSessionSerializer(serializers.ModelSerializer):
    # Показывает детали фильма вместо id
    film_title = serializers.CharField(source='film.title', read_only=True)
    film_description = serializers.CharField(source='film.description', read_only=True)
    # Показывает детали зала вместо id
    hall_name = serializers.CharField(source='hall.name', read_only=True)
    hall_capacity = serializers.CharField(source='hall.capacity', read_only=True)

    class Meta:
        model = MovieSession
        fields = [
            'id', 'film', 'film_title', 'film_description',
            'hall', 'hall_name', 'hall_capacity',
            'start_time', 'end_time', 'price'
        ]