import logging


class BaseFilterService:
    def __init__(self, name, keywords, skip_resumo: bool = True):
        self.name = name
        self.keywords = [kw.lower() for kw in keywords]
        self.skip_resumo = skip_resumo

    def match(self, text: str) -> bool:
        return any(kw in text.lower() for kw in self.keywords)

    def filter(self, items: list[dict]) -> list[dict]:
        """Recebe uma lista de itens e retorna apenas os que deram match."""
        logging.info(f"[{self.name}] iniciando filtragem...")
        resultados = []
        for item in items:
            if self.skip_resumo and not item.get("resumo"):
                continue
            if self.match(item.get("titulo", "")):
                logging.info(f"[{self.name}] MATCH: {item['titulo']}")
                resultados.append(item)
            else:
                logging.debug(f"[{self.name}] Ignorado: {item['titulo']}")
        logging.info(
            f"[{self.name}] filtragem concluída. {len(resultados)} itens encontrados."
        )
        return resultados
