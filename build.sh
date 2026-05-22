pyinstaller --clean --noconfirm --onedir --console --icon "static/logo.ico" --name "Argos" --log-level "INFO" --add-data "templates/;templates/" --add-data "static/;static/"  "server.py"
