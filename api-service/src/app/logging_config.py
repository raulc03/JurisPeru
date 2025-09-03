import logging
from app.configs.config import get_settings


def setup_logging():
    settings = get_settings()
    level = logging.INFO

    if settings.log_level == "ERROR":
        level = logging.ERROR
    elif settings.log_level == "DEBUG":
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
    )
