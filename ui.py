import customtkinter as tk

from pipeline import execute_pipeline


def on_submit():
    termo = text.get().strip()
    if termo:  # só executa se não estiver vazio
        execute_pipeline(termo)


def main():
    app = tk.CTk()
    app.title("Busca")
    app.geometry("400x200")

    # Variável de texto
    global text
    text = tk.StringVar()

    # Label
    label = tk.CTkLabel(app, text="Digite o termo de pesquisa:")
    label.pack(padx=20, pady=(20, 5))

    # Campo de entrada
    text_input = tk.CTkEntry(app, textvariable=text, width=300)
    text_input.pack(padx=20, pady=10)

    # Botão de envio
    btn_submit = tk.CTkButton(app, command=on_submit, text="Buscar")
    btn_submit.pack(padx=20, pady=20)

    app.mainloop()


if __name__ == "__main__":
    main()
