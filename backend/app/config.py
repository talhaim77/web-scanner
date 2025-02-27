import os
import logging

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Validate that the level is one of the allowed values
if LOG_LEVEL not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    LOG_LEVEL = "INFO"

def configure_logging():
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
