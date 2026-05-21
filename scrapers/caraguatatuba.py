import json
import logging
import re
from urllib.parse import quote_plus

import pandas as pd
import parsel
import requests


def main(search_term: str):
    # Configuração do logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs/scraping_caraguatatuba.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )

    # SEARCH_URL = "https://www.caraguatatuba.sp.gov.br/pmc/page/{}/?s=Educa%C3%A7%C3%A3o+Ambiental"
    SEARCH_URL = "https://www.caraguatatuba.sp.gov.br/pmc/page/{}/?s=" + quote_plus(
        search_term
    )

    logging.info(
        "Iniciando o processo de scraping de notícias sobre Educação Ambiental."
    )

    resultados = []

    try:
        logging.info("Buscando a primeira página de resultados...")
        primeira_pagina = requests.get(SEARCH_URL.replace(r"page/{}/", ""))
        primeira_pagina.raise_for_status()
        logging.info("Primeira página carregada com sucesso.")
    except requests.RequestException as e:
        logging.error(f"Erro ao buscar primeira página: {e}")
        raise

    sel = parsel.Selector(primeira_pagina.text)

    logging.info("Analisando a paginação...")
    pagination = sel.xpath(".//ul[contains(@class,'pagination')]/li")
    if pagination:
        pagination_text = pagination[-3].xpath("./a/text()").get().strip()
        pagination = int(pagination_text)
        logging.info(f"Número total de páginas encontradas: {pagination}")
    else:
        logging.warning("Paginação não encontrada. Assumindo apenas uma página.")
        pagination = 1

    noticias = sel.xpath(
        ".//div[contains(@id, 'latestNews')]/.//div[contains(@class,'row')]"
    )
    logging.info(f"Notícias encontradas na primeira página: {len(noticias)}")

    for i in range(2, pagination + 1):
        try:
            logging.info(f"Buscando página {i} de {pagination}...")
            p = requests.get(SEARCH_URL.format(i))
            p.raise_for_status()
            logging.info(f"Página {i} carregada com sucesso.")
        except requests.RequestException as e:
            logging.error(f"Erro ao buscar página {i}: {e}")
            continue

        s = parsel.Selector(p.text)
        news = s.xpath(
            ".//div[contains(@id, 'latestNews')]/.//div[contains(@class,'row')]"
        )
        if news:
            noticias.extend(news)
            logging.debug(f"Encontradas {len(news)} notícias adicionais na página {i}")
        else:
            logging.warning(f"Nenhuma notícia encontrada na página {i}")

    logging.info(f"Total de notícias coletadas: {len(noticias)}")

    def clean_text(text: str):
        return text.strip()

    logging.info("Iniciando extração de dados das notícias...")
    for noticia in noticias:
        titulo = clean_text(noticia.xpath(".//h5/a/text()").get())
        logging.info(f"Processando notícia: {titulo}")
        logging.debug(f"Título encontrado: {titulo}")

        link = clean_text(noticia.xpath(".//h5/a/@href").get())
        logging.debug(f"Link encontrado: {link}")

        data = clean_text(
            noticia.xpath(".//span[contains(@class,'created-at')]/text()").getall()[1]
        )
        match_data = re.search(r"\d{1,2}/\d{1,2}/20\d{2}", data)
        if match_data:
            data = match_data.group()
            logging.debug(f"Data encontrada: {data}")
        else:
            logging.warning(
                f"Data não encontrada no formato esperado para notícia: {titulo}"
            )
            data = "N/A"

        resumo = clean_text(
            noticia.xpath(".//div[contains(@class, 'news-text')]/p/text()").get()
        )
        logging.debug(f"Resumo encontrado: {resumo}")

        resultados.append(
            {
                "titulo": titulo,
                "data": data,
                "ano": data.split("/")[-1] if data != "N/A" else "N/A",
                "link": link,
                "resumo": resumo,
            }
        )
        logging.debug(f"Notícia '{titulo}' adicionada aos resultados.")

    logging.info(
        f"Extração concluída. Total de notícias processadas: {len(resultados)}"
    )

    logging.info("Salvando resultados no arquivo teste.json...")
    with open("json/dados_caraguatatuba_bruto.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    logging.info("Arquivo teste.json salvo com sucesso.")

    pd.DataFrame(resultados).to_excel("xlsx/dados_caraguatatuba_bruto.xlsx")

    return "json/dados_caraguatatuba_bruto.json"
