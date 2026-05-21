import re
from urllib.parse import quote_plus

import parsel
import requests

from models.noticia import Noticia
from services.scrapers.scraper_base import ScraperStrategy


class SaoSebastiaoScraper(ScraperStrategy):
    NAME = "São Sebastião"

    BASE_URL = "https://www.saosebastiao.sp.gov.br/"

    PAGINATION_XPATH = ".//div[contains(@id,'news_paging')]/li"
    NEWS_XPATH = ".//div[contains(@id, 'page-content')]/.//article"
    TITLE_XPATH = ".//h2/a/text()"
    LINK_XPATH = ".//h2/a/@href"
    DATA_XPATH = ".//div[contains(@class,'notice-date')]/text()"

    DATA_REGEX = r"\d{1,2}/\d{1,2}/20\d{2}"

    def __get_page(
        self,
        url: str,
        page: int | None = None,
    ) -> parsel.Selector:

        try:
            url_final = url.format(page) if page else url.replace(r"&pg={}", "")

            self.logger.info(
                "Buscando página %s...",
                page or 1,
            )

            response = self._get(url_final)

            self.logger.info(
                "Página %s carregada com sucesso.",
                page or 1,
            )

            return parsel.Selector(response.text)

        except requests.RequestException as e:
            self.logger.error(
                "Erro ao buscar página %s: %s",
                page or 1,
                e,
            )

            raise

    def __check_for_pagination(
        self,
        page: parsel.Selector,
    ) -> int:

        self.logger.info("Analisando paginação...")

        pagination = page.xpath(self.PAGINATION_XPATH)

        if pagination:
            pagination_text = pagination[-2].xpath("./a/text()").get()

            total = int(pagination_text.strip()) if pagination_text else 1

            self.logger.info(
                "Número total de páginas encontradas: %s",
                total,
            )

        else:
            self.logger.warning(
                "Paginação não encontrada. Assumindo apenas uma página."
            )

            total = 1

        return total

    def __get_news(
        self,
        page: parsel.Selector,
    ) -> parsel.SelectorList:

        result = page.xpath(self.NEWS_XPATH)

        self.logger.info(
            "Notícias encontradas na página: %s",
            len(result),
        )

        return result

    @staticmethod
    def __clean_text(
        text: str | None,
    ) -> str:

        return text.strip() if text else ""

    def __extract_title(
        self,
        noticia: parsel.Selector,
    ) -> str:

        titulo = self.__clean_text(noticia.xpath(self.TITLE_XPATH).get())

        self.logger.debug(
            "Título encontrado: %s",
            titulo,
        )

        return titulo

    def __extract_link(
        self,
        noticia: parsel.Selector,
    ) -> str:

        link = self.BASE_URL + self.__clean_text(noticia.xpath(self.LINK_XPATH).get())

        self.logger.debug(
            "Link encontrado: %s",
            link,
        )

        return link

    def __extract_data(
        self,
        noticia: parsel.Selector,
        noticia_titulo: str,
    ) -> tuple[str, str]:

        data_list = noticia.xpath(self.DATA_XPATH).getall()

        data = self.__clean_text(data_list[1]) if len(data_list) > 1 else ""

        match_data = re.search(
            self.DATA_REGEX,
            data,
        )

        if match_data:
            data = match_data.group()

            self.logger.debug(
                "Data encontrada: %s",
                data,
            )

        else:
            self.logger.warning(
                "Data não encontrada para notícia: %s",
                noticia_titulo,
            )

            data = "N/A"

        return (
            data,
            data.split("/")[-1] if data != "N/A" else "N/A",
        )

    def __build_response(
        self,
        news_list: parsel.SelectorList,
    ) -> list[Noticia]:

        resultados: list[Noticia] = []

        self.logger.info("Iniciando extração das notícias...")

        for noticia in news_list:
            titulo = self.__extract_title(noticia)

            self.logger.info(
                "Processando notícia: %s",
                titulo,
            )

            data, ano = self.__extract_data(
                noticia,
                titulo,
            )

            resultados.append(
                Noticia(
                    titulo=titulo or "Sem título",
                    data=data,
                    ano=ano,
                    link=self.__extract_link(noticia),
                    resumo="",
                    origem=self.NAME,
                )
            )

            self.logger.debug(
                "Notícia '%s' adicionada.",
                titulo,
            )

        return resultados

    def scrape(self, search_term: str, profundidade: int) -> list[Noticia]:

        search_url = (
            "https://www.saosebastiao.sp.gov.br/noticia-lista.asp?idTitulo="
            + quote_plus(search_term)
            + "&pg={}"
        )

        self.logger.info(
            "Iniciando scraping sobre '%s'",
            search_term,
        )

        primeira_pagina = self.__get_page(search_url)

        pagination = self.__check_for_pagination(primeira_pagina)

        noticias = self.__get_news(primeira_pagina)

        for i in range(
            2, (pagination if pagination < profundidade else profundidade) + 1
        ):
            page = self.__get_page(
                search_url,
                i,
            )

            news = self.__get_news(page)

            if news:
                noticias.extend(news)

                self.logger.debug(
                    "%s notícias encontradas na página %s",
                    len(news),
                    i,
                )

            else:
                self.logger.warning(
                    "Nenhuma notícia encontrada na página %s",
                    i,
                )

        self.logger.info(
            "Total de notícias coletadas: %s",
            len(noticias),
        )

        resultados = self.__build_response(noticias)

        self.logger.info(
            "Scraping concluído. %s notícias processadas.",
            len(resultados),
        )

        return resultados
