from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.film import FilmList, FilmDetail
from services.film import FilmService, get_film_service
from .dependencies import common_list_params


router = APIRouter()


@router.get('/')
async def index(
    film_service: FilmService = Depends(get_film_service),
    params: dict = Depends(common_list_params),
    sort: str = '-imdb_rating',
    genre: str | None = None,
) -> list[FilmList]:
    films = await film_service.get_list(**params, sort=sort, genre=genre)
    return films


@router.get('/search/')
async def film_search(
    film_service: FilmService = Depends(get_film_service),
    params: dict = Depends(common_list_params),
    query: str | None = None
) -> list[FilmList]:
    films = await film_service.get_list(**params, query=query)
    return films


@router.get('/{film_id}/')
async def film_detail(
    film_id: str,
    film_service: FilmService = Depends(get_film_service)
) -> FilmDetail:
    film = await film_service.get_detail(film_id=film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return film
