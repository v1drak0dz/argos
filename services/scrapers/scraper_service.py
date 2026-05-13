import asyncio
import logging


class ScraperService:
    def __init__(self, msgqueue):
        self.msgqueue = msgqueue
        self.queue = msgqueue.get("DOWNLOADER")

    async def run(self):
        logging.info("[ScraperService] iniciado e aguardando mensagens...")
        while True:
            payload = await self.queue.get()
            try:
                term = payload["term"]
                sites = payload["sites"]

                logging.info(f"[ScraperService] Rodando scrapers para termo: {term}")

                for scraper_cls in sites:
                    try:
                        scraper = scraper_cls()
                        result_file = scraper.scrape(term)
                        logging.info(
                            f"[ScraperService] Scraper {scraper_cls.__name__} finalizado"
                        )

                        # envia para fila de filtro
                        self.msgqueue.put(
                            "FILTER",
                            {"source": scraper_cls.__name__, "file": result_file},
                        )

                        self.msgqueue.put(
                            "STORAGE",
                            {
                                "site": scraper_cls.__name__,
                                "term": term,
                                "data": resultado,
                            },
                        )

                        # atualiza status
                        self.msgqueue.put(
                            "STATUS",
                            {
                                "step": "scrape",
                                "site": scraper_cls.__name__,
                                "status": "ok",
                            },
                        )

                    except Exception as e:
                        logging.error(
                            f"[ScraperService] Erro no scraper {scraper_cls.__name__}: {e}"
                        )
                        self.msgqueue.put(
                            "SCRAPE_ERROR",
                            {"site": scraper_cls.__name__, "error": str(e)},
                        )

            finally:
                self.queue.task_done()
