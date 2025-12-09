from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FilmViewSet, CinemaHallViewSet, MovieSessionViewSet

router = DefaultRouter()
router.register(r'films', FilmViewSet)
router.register(r'halls', CinemaHallViewSet)
router.register(r'sessions', MovieSessionViewSet)

urlpatterns = [
    path('', include(router.urls))

]