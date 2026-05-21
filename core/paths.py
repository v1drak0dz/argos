import os
import sys


def base_path():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS

    return os.path.abspath(".")


BASE_DIR = base_path()
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STORAGE_FILE = os.path.join(BASE_DIR, "job_history.json")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
