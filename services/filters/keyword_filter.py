from models.noticia import Noticia
from services.filters.filters_base import FilterStrategy


class KeywordFilter(FilterStrategy):
    def __init__(self, keywords: list[str], skip_resumo: bool = False):
        self.__keywords = [kw.lower() for kw in keywords]
        self.__skip_resumo = skip_resumo

    def filter_match(self, noticia: Noticia) -> bool:
        if not self.__skip_resumo:
            return any(
                kw in noticia.titulo.lower() or kw in noticia.resumo.lower()
                for kw in self.__keywords
            )
        else:
            return any(kw in noticia.titulo.lower() for kw in self.__keywords)
