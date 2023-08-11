from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import FilmList, FilmDetail


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.index = 'movies'

    async def get_list(
        self,
        from_ind: int,
        limit: int,
        sort: str | None = None,
        genre: str | None = None,
        query: str | None = None,
    ) -> list[FilmList]:
        body = {}
        if query:
            self._elastic_query_title_search(body, query)
        if sort:
            self._elastic_query_order_by(body, sort)
        if genre:
            self._elastic_query_genre_filter(body, genre)
        doc = await self.elastic.search(
            index=self.index,
            size=limit,
            from_=from_ind,
            body=body,
        )
        return [FilmList(**i['_source']) for i in doc['hits']['hits']]

    async def get_detail(self, film_id: str) -> Optional[FilmDetail]:
        try:
            doc = await self.elastic.get(index=self.index, id=film_id)
        except NotFoundError:
            return None
        return FilmDetail(**doc['_source'])

    def _elastic_query_order_by(self, body: dict, order_field: str) -> None:
        desc = False
        if order_field[0] == '-':
            order_field = order_field[1:]
            desc = True
        if order_field not in FilmList.model_fields:
            return
        order_query = {
            'query': {
                'match_all': {}
            },
            'sort': [
                {
                    order_field: {
                        'order': 'desc' if desc else 'asc'
                    }
                }
            ]
        }
        body.update(order_query)

    def _elastic_query_title_search(self, body: dict, search_param: str) -> None:
        search_query = {
            'query': {
                'match': {
                    'title': {
                        'query': search_param,
                        'fuzziness': 2
                    }
                }
            }
        }
        body.update(search_query)

    def _elastic_query_genre_filter(self, body: dict, filter_param: str) -> None:
        filter_query = {
            'query': {
                'bool': {
                    'must': {
                        'match': {
                            'genre': filter_param
                        }
                    }
                }
            }
        }
        body.update(filter_query)


def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
