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

    VERBOS_PRESENTE = [
        "realiza",
        "promove",
        "implanta",
        "executa",
        "conclui",
        "entrega",
        "inicia",
        "desenvolve",
        "capacita",
        "ocorre",
        "acontece",
        "participa",
        "é realizado",
        "é implantado",
        "é concluído",
        "são realizados",
        "são implantados",
        "são concluídos",
    ]

    def have_present_verb(text: str):
        return any([keyword in text.lower() for keyword in VERBOS_PRESENTE])

    filtered = []

    for item in data:
        if skip_resumo:
            if not item["resumo"]:
                continue
        if have_present_verb(item["titulo"]):
            filtered.append(item)

    logging.info(
        f"Filtragem concluída. Itens restantes após filtro: {len(filtered)} de {len(data)}."
    )

    filename = f"json/dados_{data_source_name}_filtrado_verbos_presente.json"
    logging.info(f"Salvando dados filtrados em {filename}...")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    logging.info(f"Arquivo {filename} salvo com sucesso.")
    pd.DataFrame(filtered).to_excel(filename.replace("json", "xlsx"))
