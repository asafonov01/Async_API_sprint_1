from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from movies.models import Filmwork, PersonFilmwork
from rest_framework.viewsets import ReadOnlyModelViewSet

from .pagination import FilmworkPagination
from .serializers import FilmworkSerializer


class FilmworkViewset(ReadOnlyModelViewSet):
    serializer_class = FilmworkSerializer
    queryset = Filmwork.objects.prefetch_related(
        'genre_film_work__genre',
        'person_film_work__person'
    ).annotate(
        actors=ArrayAgg(
            'person_film_work__person__full_name',
            filter=Q(person_film_work__role=PersonFilmwork.Roles.ACTOR)
        ),
        directors=ArrayAgg(
            'person_film_work__person__full_name',
            filter=Q(person_film_work__role=PersonFilmwork.Roles.DIRECTOR)
        ),
        writers=ArrayAgg(
            'person_film_work__person__full_name',
            filter=Q(person_film_work__role=PersonFilmwork.Roles.WRITER)
        ),
    )
    pagination_class = FilmworkPagination
