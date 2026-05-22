import json
import os

from core.paths import STORAGE_FILE


def load_tasks(tasks: dict):
    if not os.path.exists(STORAGE_FILE):
        tasks.clear()
        return

    try:
        with open(
            STORAGE_FILE,
            "r",
            encoding="utf-8",
        ) as f:
            loaded_tasks = json.load(f)

        tasks.clear()
        tasks.update(loaded_tasks)

    except (
        json.JSONDecodeError,
        OSError,
    ):
        tasks.clear()


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
