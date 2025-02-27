import logging
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def configure_logging():
    # Use a local variable to avoid modifying the global LOG_LEVEL
    level = LOG_LEVEL
    if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        level = "INFO"

    # Remove existing handlers to prevent duplicate logs
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Configure the root logger
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        force=True,  # Overwrite previous configurations
    )
