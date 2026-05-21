import logging
from pathlib import Path


class LoggerService:
    @staticmethod
    def get_logger(
        name: str,
        log_file: str,
        level: int = logging.INFO,
    ) -> logging.Logger:

        logger = logging.getLogger(name)

        # evita handlers duplicados
        if logger.handlers:
            return logger

        logger.setLevel(level)

        Path("logs").mkdir(exist_ok=True)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(
            f"logs/{log_file}",
            encoding="utf-8",
        )

        stream_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        return logger
