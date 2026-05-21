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
        "saosebastiao": SaoSebastiaoScraper(),
        "periodicoscapes": PeriodicosCapesScraper(),
    }

    def process_scraper(self, term: str, sites: list[str], profundidade: int) -> list:
        noticias: list[Noticia] = []

        for site in sites:
            noticias.extend(self.__strategies[site].scrape(term, profundidade))

        return noticias
