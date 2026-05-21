from abc import ABC, abstractmethod
from fake_useragent import FakeUserAgent
import requests
from typing import List

from models.noticia import Noticia
from services.logging.logger_service import LoggerService

class ScraperStrategy(ABC):
    """
    Base abstrata para scrapers de notícias.

    Fornece:
    - sessão HTTP compartilhada
    - logging padronizado
    - timeout padrão
    - helpers de request

    As subclasses devem implementar apenas
    a lógica específica de extração.
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": FakeUserAgent().random})

        logger_name = self.__class__.__name__

        log_file = logger_name.replace("Scraper", "").lower()

        self.logger = LoggerService.get_logger(name=logger_name, log_file=f'{log_file}.log')

    def _get(self, url: str, **kwargs) -> requests.Response:
        self.logger.debug(
            "GET %s",
            url
        )

        response = self.session.get(
            url,
            timeout=15,
            **kwargs
        )

        response.raise_for_status()

        return response

    @abstractmethod
    def scrape(self, search_term: str) -> List[Noticia]:
        """
        Executa o scraping para o termo de busca fornecido.

        :param search_term: termo de pesquisa (ex: "Educação Ambiental")
        :return: lista de objetos Noticia
        """
        pass
