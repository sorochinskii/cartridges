from typing import Any, Dict

from config import settings
from loguru import logger


def configure_logging() -> None:
    logger.remove()

    log_format = "{time:MMMM D, YYYY > HH:mm:ss} | " + \
                 "{level} | {message} | {extra}"
    rotation_policy = "10 MB"
    log_dir = settings.LOG_DIR

    handlers_config: Dict[str, Dict[str, Any]] = {
        "INFO": {
            "sink": f"{log_dir}/info/{{time:YYYY_MM_DD}}.log",
            "level": "INFO",
            "format": log_format,
            "rotation": rotation_policy,
            "filter": lambda record: record["level"].name == "INFO"
        },
        "ERROR": {
            "sink": f"{log_dir}/error/{{time:YYYY_MM_DD}}.log",
            "level": "ERROR",
            "format": log_format,
            "rotation": rotation_policy,
            "filter": lambda record: record["level"].name == "ERROR"
        }
    }

    if settings.ENVIRONMENT != "prod":
        handlers_config["DEBUG"] = {
            "sink": f"{log_dir}/debug/{{time:YYYY_MM_DD}}.log",
            "level": "DEBUG",
            "format": log_format,
            "rotation": rotation_policy,
            "filter": lambda record: record["level"].name == "DEBUG"
        }

    for handler_config in handlers_config.values():
        logger.add(**handler_config)

configure_logging()