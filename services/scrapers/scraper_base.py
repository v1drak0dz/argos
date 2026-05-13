from abc import ABC, abstractmethod


class ScraperStrategy(ABC):
    @abstractmethod
    def scrape(self, search_term: str) -> list:
        pass
