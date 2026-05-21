from models.noticia import Noticia
from services.filters.filters_base import FilterStrategy


class AnoFilter(FilterStrategy):
    def __init__(self, start_year: str, end_year: str)
        self.__start_year = start_year
        self.__end_year   = end_year

    def filter_match(self, noticia: Noticia) -> bool:
        return noticia.ano > self.__start_year and noticia.ano < self.__end_year
