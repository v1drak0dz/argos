import asyncio
import logging

from constants import PAST_VERBS, PRESENT_VERBS
from services.filter_service import BaseFilterService
from services.scrapers.caraguatatuba import CaraguatatubaScraper
from services.scrapers.sao_sebastiao import SaoSebastiaoScraper
from services.scrapers.ubatuba import UbatubaScraper


async def producer(queue: asyncio.Queue, scraper, name: str, term: str):
    """Executa um scraper e coloca os itens na fila"""
    resultados = scraper.scrape(term)
    logging.info(f"[{name}] Produtor carregou {len(resultados)} itens.")
    for item in resultados:
        await queue.put(item)
    await queue.join()


async def execute_pipeline(term: str = "Educação Ambiental"):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

    queue = asyncio.Queue()

    # Definição dos filtros
    keyword_filter = BaseFilterService(
        "KeywordFilter", ["escola", "parque", "comunidade"], queue
    )
    past_filter = BaseFilterService("PastVerbsFilter", PAST_VERBS, queue)
    present_filter = BaseFilterService("PresentVerbsFilter", PRESENT_VERBS, queue)

    # Lista de scrapers (Strategy)
    scrapers = [
        ("caraguatatuba", CaraguatatubaScraper()),
        ("sao_sebastiao", SaoSebastiaoScraper()),
        ("ubatuba", UbatubaScraper()),
    ]

    # Roda tudo junto: produtores + consumidores
    await asyncio.gather(
        *(producer(queue, scraper, name, term) for name, scraper in scrapers),
        keyword_filter.run(),
        past_filter.run(),
        present_filter.run(),
    )


if __name__ == "__main__":
    asyncio.run(execute_pipeline())
