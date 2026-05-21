import json
import logging

import pandas as pd


def main(data_source_name: str, data_source: str, skip_resumo: bool):
    # Configuração do logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(
                f"logs/filtrando_{data_source_name}.log", encoding="utf-8"
            ),
            logging.StreamHandler(),
        ],
    )

    with open(data_source, "r", encoding="utf-8") as f:
        data = json.load(f)

    logging.info(f"Dados carregados de {data_source}: {len(data)} itens.")
    logging.info(
        "Iniciando processo de filtragem baseado em verbos no presente e resumo não vazio..."
    )

    KEYWORDS = ["escola", "parque", "comunidade"]

    def have_keyword(text: str):
        return any([keyword in text.lower() for keyword in KEYWORDS])

    filtered = []

    for item in data:
        if skip_resumo:
            if not item["resumo"]:
                continue
        if have_keyword(item["titulo"]):
            filtered.append(item)

    logging.info(
        f"Filtragem concluída. Itens restantes após filtro: {len(filtered)} de {len(data)}."
    )

    filename = f"json/dados_{data_source_name}_filtrados_palavra_chave.json"
    logging.info(f"Salvando dados filtrados em {filename}...")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    logging.info(f"Arquivo {filename} salvo com sucesso.")
    pd.DataFrame(filtered).to_excel(filename.replace("json", "xlsx"))
