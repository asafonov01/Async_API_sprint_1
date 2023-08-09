from django.contrib import admin

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    autocomplete_fields = ['film_work']


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    autocomplete_fields = ['genre']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline,)
    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres')
    list_filter = ('type', )
    search_fields = ('title', 'description', )
    list_prefetch_related = ('genre_film_work__genre', )

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join([gwf.genre.name for gwf in obj.genre_film_work.all()])

    get_genres.short_description = 'Жанры фильма'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    inlines = (PersonFilmworkInline, )
    list_display = ('full_name', 'get_movies')
    search_fields = ('full_name', )
    list_prefetch_related = ('person_film_work__film_work', )

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_movies(self, obj):
        return ', '.join(
            [pfw.film_work.title for pfw in obj.person_film_work.all()]
        )

    get_movies.short_description = 'Фильмы и сериалы'
