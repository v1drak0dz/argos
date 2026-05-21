import os

import pandas as pd


def save_data(data: list, job_id: str, filename: str) -> None:
    folder_path = os.path.join("artifacts", job_id)
    os.makedirs(folder_path, exist_ok=True)

    filepath = os.path.join(folder_path, filename)
    pd.DataFrame(data).to_csv(filepath)
