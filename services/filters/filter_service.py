import logging

from models.noticia import Noticia
from services.filters.filters_base import FilterStrategy


class FilterService:
    def __init__(self, name: str, strategies: list[FilterStrategy]):
        self.__name = name
        self.__strategies = strategies

    def process_filter(self, items: list[Noticia]) -> list[Noticia]:
        logging.info("[%s] iniciando filtragem...", self.__name)
        resultados: list[Noticia] = []

        for item in items:
            if all(strategy.filter_match(item) for strategy in self.__strategies):
                logging.info("[%s] MATCH: %s", self.__name, item.titulo)
                resultados.append(item)

            else:
                logging.debug("[%s] Ignorado: %s", self.__name, item.titulo)

        logging.info(
            "[%s] filtragem concluída. %s itens encontrados.",
            self.__name,
            len(resultados),
        )
        return resultados
