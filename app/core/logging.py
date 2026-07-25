import logging
import sys

from app.core.config import settings


def configure_logging():
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(level)

    logging.getLogger("uwsgi").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO if settings.DEBUG else logging.WARNING)