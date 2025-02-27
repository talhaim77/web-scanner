import logging
from typing import Dict, Any

logger = logging.getLogger("uvicorn")


class BaseExtractor:
    """
    Base extractor class.
    """

    def extract(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts data from raw input.

        Args:
            raw_data (Dict[str, Any]): The raw data as a dictionary.

        Returns:
            Dict[str, Any]: Processed data extracted from raw_data.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        raise NotImplementedError("Extractor must implement extract method.")


class HTTPXExtractor(BaseExtractor):
    """
    Extracts and maps fields from HTTPX output.
    """

    def extract(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extracts relevant fields from HTTPX output.

        Args:
            raw_data (Dict[str, Any]): A dictionary containing HTTPX response data.
                Expected keys:
                - "a": List of IPv4 addresses.
                - "input": Domain name.
                - "title": Webpage title.
                - "status_code": HTTP response code.
                - "webserver": Web server details.
                - "tech": List of technologies used.
                - "cname": List of CNAME records.

        Returns:
            Dict[str, Any]: A dictionary with the extracted fields:
                - "domain" (str)
                - "related_ips" (list)
                - "webpage_title" (str)
                - "status_code" (int or None)
                - "webserver" (str)
                - "technologies" (list)
                - "cnames" (list)
        """
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
