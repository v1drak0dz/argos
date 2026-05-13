import customtkinter as tk

from constants import BORDER_WIDTH, CHECKBOXES_SIZE, DOWNLOADER
from services.scrapers.caraguatatuba import CaraguatatubaScraper
from services.scrapers.sao_sebastiao import SaoSebastiaoScraper
from services.scrapers.ubatuba import UbatubaScraper


class SearchUI:
    def __init__(self, msgqueue):
        self.msgqueue = msgqueue
        self.app = tk.CTk()
        self.app.title("Busca")
        self.app.geometry("450x300")

        # Variável de texto
        self.text = tk.StringVar()

        # Label + Campo de entrada
        label = tk.CTkLabel(self.app, text="Digite o termo de pesquisa:")
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="w")

        text_input = tk.CTkEntry(self.app, textvariable=self.text, width=300)
        text_input.grid(
            row=1, column=0, columnspan=2, padx=10, pady=(0, 15), sticky="ew"
        )

        # Frame para sites
        sites_frame = tk.CTkFrame(self.app)
        sites_frame.grid(
            row=2, column=0, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=10
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

        # Frame para filtros
        filters_frame = tk.CTkFrame(self.app)
        filters_frame.grid(
            row=2, column=1, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=10
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

        # Botão de envio
        btn_submit = tk.CTkButton(self.app, command=self.on_submit, text="Buscar")
        btn_submit.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

        # Ajusta proporções
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)

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

            self.msgqueue.put(
                DOWNLOADER,
                {
                    "term": termo,
                    "sites": scrapers,
                    "filters": {
                        "past": self.cb_verbos_passado.get(),
                        "present": self.cb_verbos_presente.get(),
                        "keywords": self.cb_keywords.get(),
                    },
                },
            )

    def run(self):
        self.app.mainloop()
