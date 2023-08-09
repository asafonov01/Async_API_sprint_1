from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(r'movies', views.FilmworkViewset)


urlpatterns = [
    path('', include(v1_router.urls))
]
