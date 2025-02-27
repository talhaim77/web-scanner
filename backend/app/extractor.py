from typing import Dict, Any

from app_logger import logger


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
        """

        :param raw_data:
        :return:
        """
        logger.info(f"Raw Data: {raw_data}")

        ipv4 = raw_data.get("a", [])
        ipv6 = raw_data.get("aaaa", [])
        related_ips = list(set(ipv4 + ipv6))

        extracted = {
            "domain": raw_data.get("input", ""),
            "related_ips": related_ips,
            "webpage_title": raw_data.get("title", ""),
            "status_code": raw_data.get("status_code", None),
            "webserver": raw_data.get("webserver", ""),
            "technologies": raw_data.get("tech", []),
            "cnames": raw_data.get("cname", [])
        }
        logger.info(f"Extracted Data: {extracted}")
        return extracted