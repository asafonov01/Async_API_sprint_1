from movies.models import Filmwork
from rest_framework import serializers


class GenreField(serializers.RelatedField):

    def to_representation(self, value):
        return value.genre.name


class FilmworkSerializer(serializers.ModelSerializer):

    genres = GenreField(source='genre_film_work', read_only=True, many=True)
    actors = serializers.ListField()
    directors = serializers.ListField()
    writers = serializers.ListField()

    class Meta:
        model = Filmwork
        fields = [
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
            'genres',
            'actors',
            'directors',
            'writers',
        ]
