import logging
from functools import cache

from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.cache import ModelCache, get_cache_storage, AbstractCacheStorage
from db.elastic import get_elastic
from db.models import Person
from db.storage import ElasticSearchStorage
from services.base import BaseElasticSearchService

logger = logging.getLogger(__name__)


class PersonService(BaseElasticSearchService):
    model = Person


@cache
def get_person_service(
        redis: AbstractCacheStorage = Depends(get_cache_storage),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(ModelCache(Person, redis),
                         ElasticSearchStorage(elastic=elastic, index='persons'))
