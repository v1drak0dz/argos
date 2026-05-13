import json
import logging
from pathlib import Path

import pandas as pd


class StorageService:
    @staticmethod
    def save(site: str, term: str, data: list[dict]):
        if not data:
            logging.warning("[StorageService] Nenhum dado para salvar")
            return

        # Cria pastas se não existirem
        Path("json").mkdir(exist_ok=True)
        Path("xlsx").mkdir(exist_ok=True)

        # Salva JSON
        json_file = f"json/{site}_{term}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logging.info(f"[StorageService] JSON salvo em {json_file}")

        # Salva XLSX
        xlsx_file = f"xlsx/{site}_{term}.xlsx"
        pd.DataFrame(data).to_excel(xlsx_file, index=False)
        logging.info(f"[StorageService] XLSX salvo em {xlsx_file}")
