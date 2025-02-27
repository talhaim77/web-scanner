import logging
from typing import Dict, Any

logger = logging.getLogger("uvicorn")


class BaseExtractor:
    """
    Base extractor class.
    """

    def extract(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("Extractor must implement extract method.")


class HTTPXExtractor(BaseExtractor):
    """
    Extracts and maps fields from HTTPX output.
    """

    def extract(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        ipv4 = raw_data.get("a", [])

        extracted = {
            "domain": raw_data.get("input", ""),
            "related_ips": ipv4,
            "webpage_title": raw_data.get("title", ""),
            "status_code": raw_data.get("status_code", None),
            "webserver": raw_data.get("webserver", ""),
            "technologies": raw_data.get("tech", []),
            "cnames": raw_data.get("cname", []),
        }
        logger.debug(f"Extracted Data: {extracted}")
        return extracted
