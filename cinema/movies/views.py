from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Film, FavoriteFilm, CinemaHall, MovieSession
from .serializers import FilmSerializer, FavoriteFilmSerializer, CinemaHallSerializer, MovieSessionSerializer


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all().order_by('release_year')
    serializer_class = FilmSerializer


    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None,):
        film = self.get_object()
        user = User.objects.first()

        if request.method == 'POST':
            favorite, created = FavoriteFilm.objects.get_or_create(
                user=user,
                film=film,
            )

            if created:
                return Response({
                    'status': 'added',
                    'message': f'Фильм "{film.title}" добавлен в избранное'
                }, status = status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': 'already in favorite',
                    'message': f'Фильм "{film.title}" уже в избранном'
                }, status = status.HTTP_200_OK)
        elif request.method == 'DELETE':
            try:
                favorite = FavoriteFilm.objects.get(film=film, user=user)
                favorite.delete()
                return Response({
                    'status': 'deleted',
                    'message': f'Фильм"{film.title}" удален из избранного'
                }, status = status.HTTP_200_OK)
            except FavoriteFilm.DoesNotExist:
                return Response({
                    'status': 'not found',
                    'message': 'Фильм не найден в избранном'
                }, status = status.HTTP_404_NOT_FOUND)


    @action(detail=False, methods=['get'])
    def my_favorites(self, request):
        user = User.objects.first()


        favorites = FavoriteFilm.objects.filter(user=user).select_related('film')
        serializer = FavoriteFilmSerializer(favorites, many=True)

        return Response({
            'count': favorites.count(),
            'results': serializer.data

        })


    @action (detail=True, methods=['get'])
    def is_favorite(self, request, pk=None):
        film = self.get_object()
        user = User.objects.first()
        is_favorite = FavoriteFilm.objects.filter(user=user, film=film).exists()

        return Response({
            'film_id': film.id,
            'film_title': film.title,
            'is_favorite': is_favorite
        })


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer

    @action(detail=True, methods=['get'])
    def hall_info(self, request, pk=None):
        hall = self.get_object()
        return Response({
            'name': hall.name,
            'capacity': hall.capacity,
            'available_seats': hall.capacity,
            'has_3d': hall.has_3d
        })



class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.all().select_related('film', 'hall')
    serializer_class = MovieSessionSerializer

    @action(detail=False, methods=['get'])
    def today_sessions(self, request):
        """Сегодняшние сеансы"""
        from django.utils import timezone
        today = timezone.now().date()

        today_session = MovieSession.objects.filter(
            start_time__date=today,
        ).select_related('film', 'hall')

        serializer = self.get_serializer(today_session, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_film(self, request):
        """ сеанс по фильму"""
        film_id = request.GET.get('film_id')
        if not film_id:
            return Response({'error': 'Укажите film_id'}, status = 400)

        sessions = MovieSession.objects.filter(
            film_id=film_id,
        ).select_related('film', 'hall')

        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_hall(self, request):
        """сеанс по залу"""
        hall_id = request.GET.get('hall_id')
        if not hall_id:
            return Response({'error': 'Укажи hall_id'}, status = 400)
        sessions = MovieSession.objects.filter(
            hall_id=hall_id,
        ).select_related('film', 'hall')

        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)