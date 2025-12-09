from django.contrib.auth.models import User
from django.db import models

class Film(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назавние фильма")
    release_year = models.PositiveSmallIntegerField(verbose_name="Год выпуска")
    duration = models.PositiveSmallIntegerField(verbose_name="Длительность фильма(мин.)")
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class FavoriteFilm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name="Фильм")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Избранный фильм"
        verbose_name_plural = "Избранные фильмы"
        unique_together = ("user", "film")

    def __str__(self):
        return f"{self.user.username} - {self.film.title}"



class CinemaHall(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название зала")
    capacity = models.PositiveSmallIntegerField(verbose_name="Вместимость")
    has_3d = models.BooleanField(default=False, verbose_name="3D")

    def __str__(self):
        return f"{self.name} ({self.capacity} мест)"

    class Meta:
        verbose_name = "Кинозал"
        verbose_name_plural = "Кинозалы"



class MovieSession(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name="Фильм")
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, verbose_name="Зал")
    start_time = models.DateTimeField(verbose_name="Начало фильма")
    end_time = models.DateTimeField(verbose_name="Конец фильма")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена билета")

    def __str__(self):
        return f"{self.film.title} - {self.hall.name} ({self.start_time.strftime('%Y/%m/%d')})"

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"
        ordering = ['start_time']