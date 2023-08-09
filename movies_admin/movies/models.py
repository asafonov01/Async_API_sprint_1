import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = '"content\".\"genre"'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):

    class TypeChoices(models.TextChoices):
        MOVIE = 'movie', _('movie')
        TV_SHOW = 'tv_show', _('tv_show')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateField(
        _('creation_date'),
        db_index=True,
        null=True
    )
    rating = models.IntegerField(
        _('rating'),
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        null=True,
    )
    certificate = models.CharField(
        _('certificate'),
        max_length=512,
        blank=True,
        null=True,
    )
    file_path = models.FileField(
        _('file'),
        blank=True,
        null=True,
        upload_to='movies/'
    )
    type = models.CharField(
        _('type'),
        max_length=128,
        choices=TypeChoices.choices,
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = '"content\".\"film_work"'
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'
        indexes = [
            models.Index(
                fields=['creation_date'],
                name='film_work_creation_date_idx'
            )
        ]


class GenreFilmwork(UUIDMixin):
    film_work = models.ForeignKey(
        Filmwork,
        on_delete=models.CASCADE,
        related_name='genre_film_work'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre_film_work'
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"content\".\"genre_film_work"'
        constraints = (
            models.UniqueConstraint(
                fields=('genre_id', 'film_work_id'),
                name='genre_film_work_idx'
            ),
        )


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        db_table = '"content\".\"person"'
        verbose_name = 'Персонаж'
        verbose_name_plural = 'Персонажи'


class PersonFilmwork(UUIDMixin):

    class Roles(models.TextChoices):
        WRITER = 'writer', _('writer')
        DIRECTOR = 'director', _('director')
        ACTOR = 'actor', _('actor')

    film_work = models.ForeignKey(
        Filmwork,
        on_delete=models.CASCADE,
        related_name='person_film_work'
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='person_film_work'
    )
    role = models.CharField(
        _('role'),
        max_length=128,
        choices=Roles.choices,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = '"content\".\"person_film_work"'
