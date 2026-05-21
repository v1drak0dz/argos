import re
from typing import Optional
from urllib.parse import quote_plus

from parsel import SelectorList
from parsel.selector import Selector
from requests.exceptions import RequestException

from models.noticia import Noticia
from services.scrapers.scraper_base import ScraperStrategy


class PeriodicosCapesScraper(ScraperStrategy):
    NAME = "Periodicos Capes"

    SEARCH_URL = (
        "https://www.periodicos.capes.gov.br/index.php/acervo/buscador.html"
        "?q=all:contains({})&type[]=type==Artigo&publishyear_min[]=1969&publishyear_max[]=2027&mode=advanced&source=all"
    )
    PAGINATION_XPATH = ".//div[contains(@class,'pagination-information')]/.//span[contains(@class,'total')]/text()"
    NEWS_XPATH = (
        ".//div[contains(@id,'resultados')]/.//div[contains(@id,'result-busca')]"
    )
    TITLE_XPATH = ".//a[contains(@class,'titulo-busca')]/text()"
    LINK_XPATH = ".//a[contains(@class,'titulo-busca')]/@href"

    # &page={}

    def __get_page(self, url: str, page: Optional[int] = None) -> Selector:
        try:
            self.logger.info("Buscando página %s...", page or 1)
            url_final = url + f"&page={page}" if page else url
            response = self._get(url_final)
            self.logger.info("Página %s carregada com sucesso.", page or 1)
            return Selector(response.text)
        except RequestException as ex:
            self.logger.error("Erro ao buscar página %s: %s", page or 1, ex)
            raise

    def __check_for_pagination(self, page: Selector) -> int:
        self.logger.info("Analisando paginação...")
        pagination = page.xpath(self.PAGINATION_XPATH)
        if pagination:
            total = int(pagination.get().strip()) // 30
            self.logger.info("Número total de páginas encontradas: %s", total)
        else:
            self.logger.warning(
                "Paginação não encontrada. Assumindo apenas uma página."
            )
            total = 1
        return total

    def __get_news(self, page: Selector) -> SelectorList:
        result = page.xpath(self.NEWS_XPATH)
        self.logger.info("Notícias encontradas: %s", len(result))
        return result

    def __extract_title(self, noticia: Selector) -> str:
        titulo = noticia.xpath(self.TITLE_XPATH).get()
        self.logger.debug("Título encontrado: %s", titulo)
        return titulo

    def __extract_link(self, noticia: Selector) -> str:
        link = noticia.xpath(self.LINK_PATH).get()
        self.logger.debug("Link encontrado: %s", link)
        return link

    def __extract_data(self, noticia: Selector, titulo: str) -> tuple[str, str]:
        texts = noticia.xpath(".//p[contains(@class,'text-down-01')]")
        if len(texts) > 1:
            mat = re.match(r"\d{4}", texts[1].get())
            if mat:
                return mat.group()
        else:
            return ""

    def __extract_resumo(self, noticia: Selector) -> str:
        resumo = noticia.xpath(".//blockquote/p/text()").get()
        self.logger.debug("Resumo encontrado: %s", resumo)
        return resumo

    def __build_response(self, news_list: SelectorList) -> list[Noticia]:
        resultados = []
        self.logger.info("Iniciando extração das notícias...")
        for noticia in news_list:
            titulo = self.__extract_title(noticia)
            self.logger.info("Processando notícia: %s", titulo)

            ano = self.__extract_data(noticia, titulo)
            resultados.append(
                Noticia(
                    titulo=titulo,
                    data="",
                    ano=ano,
                    link=self.__extract_link(noticia),
                    resumo=self.__extract_resumo(noticia),
                    origem=self.NAME,
                )
            )

            self.logger.debug("Notícia '%s' adicionada.", titulo)
        return resultados

    def scrape(self, search_term: str, profundidade: int) -> list[Noticia]:
        self.logger.info("Iniciando scraping sobre '%s'", search_term)

        primeira_pagina = self.__get_page(
            self.SEARCH_URL.format(quote_plus(search_term))
        )
        pagination = self.__check_for_pagination(primeira_pagina)
        noticias = self.__get_news(primeira_pagina)
        for i in range(
            2, (pagination if pagination < profundidade else profundidade) + 1
        ):
            page = self.__get_page(self.SEARCH_URL.format(quote_plus(search_term)), i)
            news = self.__get_news(page)
            if news:
                noticias.extend(news)
                self.logger.debug("%s notícias encontradas na página %s", len(news), i)
            else:
                self.logger.warning("Nenhuma notícia encontrada na página %s", i)

        self.logger.info("Total de notícias coletadas: %%s", len(noticias))
        resultados = self.__build_response(noticias)

        self.logger.info(
            "Scraping concluído. %s notícias processadas.", len(resultados)
        )
        return resultados
