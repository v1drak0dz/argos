import asyncio
import json
import logging
from pathlib import Path

import pandas as pd


class StorageService:
    def __init__(self, msgqueue):
        self.msgqueue = msgqueue
        self.queue = msgqueue.get("STORAGE")

    async def run(self):
        logging.info("[StorageService] iniciado e aguardando mensagens...")
        while True:
            item = await self.queue.get()
            try:
                # item deve ser uma lista de dicts ou um dict com 'data'
                data = item.get("data")
                site = item.get("site", "default")
                term = item.get("term", "search")

                if not data:
                    logging.warning("[StorageService] Nenhum dado para salvar")
                    continue

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

                # Atualiza status
                self.msgqueue.put(
                    "STATUS", {"step": "storage", "site": site, "status": "ok"}
                )

            except Exception as e:
                logging.error(f"[StorageService] Erro ao salvar dados: {e}")
                self.msgqueue.put("STORAGE_ERROR", {"error": str(e)})
            finally:
                self.queue.task_done()
