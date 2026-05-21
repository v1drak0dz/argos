import json
import os

from core.config import STORAGE_FILE

def load_tasks():
    global tasks

    if not os.path.exists(STORAGE_FILE):
        tasks = {}
        return

    try:
        with open(
            STORAGE_FILE,
            "r",
            encoding="utf-8",
        ) as f:
            tasks = json.load(f)

    except (
        json.JSONDecodeError,
        OSError,
    ):
        tasks = {}


def save_tasks_snapshot(
    snapshot: dict,
):
    temp_file = f"{STORAGE_FILE}.tmp"

    with open(
        temp_file,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            snapshot,
            f,
            ensure_ascii=False,
            indent=4,
        )

    os.replace(
        temp_file,
        STORAGE_FILE,
    )