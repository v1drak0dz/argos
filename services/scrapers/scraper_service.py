from models.noticia import Noticia
from services.scrapers.caraguatatuba import CaraguatatubaScraper
from services.scrapers.periodicos_capes import PeriodicosCapesScraper
from services.scrapers.sao_sebastiao import SaoSebastiaoScraper
from services.scrapers.scraper_base import ScraperStrategy
from services.scrapers.ubatuba import UbatubaScraper


class ScraperService:
    __strategies: dict[str, ScraperStrategy] = {
        "caraguatatuba": CaraguatatubaScraper(),
        "ubatuba": UbatubaScraper(),
        "sao_sebastiao": SaoSebastiaoScraper(),
        "periodicos_capes": PeriodicosCapesScraper(),
    }

    def process_scraper(self, term: str, sites: list[str]) -> list:
        noticias: list[Noticia] = []
        for site in sites:
            noticias.extend(self.__strategies[site].scrape(term))

        return noticias
