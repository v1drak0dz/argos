import logging
from tkinter import PhotoImage

import customtkinter as tk

from constants import BORDER_WIDTH, CHECKBOXES_SIZE, PAST_VERBS, PRESENT_VERBS
from services.scrapers.caraguatatuba import CaraguatatubaScraper
from services.scrapers.sao_sebastiao import SaoSebastiaoScraper
from services.scrapers.ubatuba import UbatubaScraper
from services.storage_service import StorageService


class SearchUI:
    def __init__(self):
        self.app = tk.CTk()
        self.app.title("Busca por dados em noticias")
        self.app.geometry("450x300")
        icon = "icon.png"
        self.app.iconphoto(False, PhotoImage(file=icon))

        self.text = tk.StringVar()
        self.keywords = ["escola", "parque", "comunidade"]  # padrão inicial

        label = tk.CTkLabel(self.app, text="Digite o termo de pesquisa:")
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        text_input = tk.CTkEntry(self.app, textvariable=self.text, width=300)
        text_input.grid(
            row=1, column=0, columnspan=4, padx=10, pady=(0, 15), sticky="ew"
        )

        # Checkboxes de sites
        sites_frame = tk.CTkFrame(self.app)
        sites_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew",
            ipadx=10,
            ipady=10,
        )

        tk.CTkLabel(sites_frame, text="Sites para buscar:").grid(
            row=0, column=0, sticky="w", padx=10
        )
        self.cb_caragua = tk.CTkCheckBox(
            sites_frame,
            text="Caraguatatuba",
            checkbox_height=CHECKBOXES_SIZE,
            checkbox_width=CHECKBOXES_SIZE,
            border_width=BORDER_WIDTH,
        )
        self.cb_caragua.grid(row=1, column=0, sticky="w", padx=10)

        self.cb_ubatuba = tk.CTkCheckBox(
            sites_frame,
            text="Ubatuba",
            checkbox_height=CHECKBOXES_SIZE,
            checkbox_width=CHECKBOXES_SIZE,
            border_width=BORDER_WIDTH,
        )
        self.cb_ubatuba.grid(row=2, column=0, sticky="w", padx=10)

        self.cb_saosebastiao = tk.CTkCheckBox(
            sites_frame,
            text="São Sebastião",
            checkbox_height=CHECKBOXES_SIZE,
            checkbox_width=CHECKBOXES_SIZE,
            border_width=BORDER_WIDTH,
        )
        self.cb_saosebastiao.grid(row=3, column=0, sticky="w", padx=10)

        # Checkboxes de filtros
        filters_frame = tk.CTkFrame(self.app)
        filters_frame.grid(
            row=2,
            column=2,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew",
            ipadx=10,
            ipady=10,
        )

        tk.CTkLabel(filters_frame, text="Filtros:").grid(
            row=0, column=0, sticky="w", padx=10
        )
        self.cb_verbos_passado = tk.CTkCheckBox(
            filters_frame,
            text="Verbos Passado",
            checkbox_height=CHECKBOXES_SIZE,
            checkbox_width=CHECKBOXES_SIZE,
            border_width=BORDER_WIDTH,
        )
        self.cb_verbos_passado.grid(row=1, column=0, sticky="w", padx=10)

        self.cb_verbos_presente = tk.CTkCheckBox(
            filters_frame,
            text="Verbos Presente",
            checkbox_height=CHECKBOXES_SIZE,
            checkbox_width=CHECKBOXES_SIZE,
            border_width=BORDER_WIDTH,
        )
        self.cb_verbos_presente.grid(row=2, column=0, sticky="w", padx=10)

        self.cb_keywords = tk.CTkCheckBox(
            filters_frame,
            text="Palavras-Chaves",
            checkbox_height=CHECKBOXES_SIZE,
            checkbox_width=CHECKBOXES_SIZE,
            border_width=BORDER_WIDTH,
        )
        self.cb_keywords.grid(row=3, column=0, sticky="w", padx=10)

        # Botão de Configurações
        btn_config = tk.CTkButton(
            self.app, command=self.open_config, text="Configurações"
        )
        btn_config.grid(row=3, column=2, columnspan=2, padx=10, pady=10)

        # Botão de envio
        btn_submit = tk.CTkButton(self.app, command=self.on_submit, text="Buscar")
        btn_submit.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_columnconfigure(2, weight=1)
        self.app.grid_columnconfigure(3, weight=1)

    def open_config(self):
        popup = tk.CTkToplevel(self.app)
        popup.title("Configurações de Filtros")
        popup.geometry("300x150")

        tk.CTkLabel(popup, text="Palavras-chave (separadas por vírgula):").pack(pady=10)
        keywords_var = tk.StringVar(value=", ".join(self.keywords))
        entry_keywords = tk.CTkEntry(popup, textvariable=keywords_var, width=250)
        entry_keywords.pack(pady=5)

        def save_keywords():
            self.keywords = [
                kw.strip().lower() for kw in keywords_var.get().split(",") if kw.strip()
            ]
            logging.info(f"Palavras-chave atualizadas: {self.keywords}")
            popup.destroy()

        btn_save = tk.CTkButton(popup, text="Salvar", command=save_keywords)
        btn_save.pack(pady=10)

    def on_submit(self):
        termo = self.text.get().strip()
        if termo:
            scrapers = []
            if self.cb_caragua.get():
                scrapers.append(CaraguatatubaScraper)
            if self.cb_ubatuba.get():
                scrapers.append(UbatubaScraper)
            if self.cb_saosebastiao.get():
                scrapers.append(SaoSebastiaoScraper)

            for scraper_cls in scrapers:
                scraper = scraper_cls()
                resultados = scraper.scrape(termo)
                logging.info(
                    f"{scraper_cls.__name__} retornou {len(resultados)} resultados"
                )

                if self.cb_verbos_passado.get():
                    filtrados = [
                        item
                        for item in resultados
                        if any(kw in item["titulo"].lower() for kw in PAST_VERBS)
                    ]
                    StorageService.save(
                        site=scraper_cls.__name__, term=termo, data=filtrados
                    )

                if self.cb_verbos_presente.get():
                    filtrados = [
                        item
                        for item in resultados
                        if any(kw in item["titulo"].lower() for kw in PRESENT_VERBS)
                    ]
                    StorageService.save(
                        site=scraper_cls.__name__, term=termo, data=filtrados
                    )

                # Aqui você pode aplicar os filtros usando self.keywords
                if self.cb_keywords.get():
                    filtrados = [
                        item
                        for item in resultados
                        if any(kw in item["titulo"].lower() for kw in self.keywords)
                    ]
                    StorageService.save(
                        site=scraper_cls.__name__, term=termo, data=filtrados
                    )
                else:
                    StorageService.save(
                        site=scraper_cls.__name__, term=termo, data=resultados
                    )

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    SearchUI().run()
