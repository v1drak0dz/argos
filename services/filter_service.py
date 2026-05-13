import logging


class BaseFilterService:
    def __init__(self, name, keywords, queue, skip_resumo: bool = True):
        self.name = name
        self.keywords = [kw.lower() for kw in keywords]
        self.queue = queue
        self.skip_resumo = skip_resumo

    def match(self, text: str) -> bool:
        return any(kw in text.lower() for kw in self.keywords)

    async def run(self):
        logging.info(f"[{self.name}] iniciado e aguardando mensagens...")
        while True:
            item = await self.queue.get()
            try:
                if self.skip_resumo and not item.get("resumo"):
                    continue
                if self.match(item.get("titulo", "")):
                    logging.info(f"[{self.name}] MATCH: {item['titulo']}")
                    # aqui você pode repassar para fila de salvamento
                else:
                    logging.debug(f"[{self.name}] Ignorado: {item['titulo']}")
            finally:
                self.queue.task_done()
