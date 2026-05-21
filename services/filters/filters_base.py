from abc import ABC, abstractmethod

from models.noticia import Noticia


class FilterStrategy(ABC):
    @abstractmethod
    def filter_match(self, noticia: Noticia) -> bool:
        """Define se a notícia deve ser aceita pelo filtro."""
        pass
