import asyncio
import threading

from constants import DOWNLOADER, FILTER, PAST_VERBS, PRESENT_VERBS, STATUS, STORAGE
from services.filter_service import BaseFilterService
from services.message_queue import MessageQueue
from services.scrapers.scraper_service import ScraperService
from services.storage_service import StorageService
from ui import SearchUI


async def run_services(msgqueue: MessageQueue):
    # Filtros
    keyword_filter = BaseFilterService(
        "KeywordFilter", ["escola", "parque", "comunidade"], msgqueue.get(FILTER)
    )
    past_filter = BaseFilterService("PastVerbsFilter", PAST_VERBS, msgqueue.get(FILTER))
    present_filter = BaseFilterService(
        "PresentVerbsFilter", PRESENT_VERBS, msgqueue.get(FILTER)
    )

    # Scraper
    scraper_service = ScraperService(msgqueue)

    storage_service = StorageService(msgqueue)

    await asyncio.gather(
        keyword_filter.run(),
        past_filter.run(),
        present_filter.run(),
        scraper_service.run(),
        storage_service.run(),
    )


def start_async_services(msgqueue: MessageQueue):
    asyncio.run(run_services(msgqueue))


if __name__ == "__main__":
    msgq = MessageQueue()
    msgq.create_queue(DOWNLOADER)
    msgq.create_queue(FILTER)
    msgq.create_queue(STORAGE)
    msgq.create_queue(STATUS)
    msgq.create_queue("SCRAPE_ERROR")  # fila de erro do scraper

    # Thread para serviços assíncronos
    t = threading.Thread(target=start_async_services, args=(msgq,), daemon=True)
    t.start()

    # Thread principal roda a UI
    ui = SearchUI(msgq)
    ui.run()
