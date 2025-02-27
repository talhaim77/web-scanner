import logging

from models import ScanResult
from typing import Dict, Any

logger = logging.getLogger("uvicorn")

class ResultBuilder:
    """
    Builder to construct ScanResult model.
    """
    def __init__(self, domain: str):
        self.result: Dict[str, Any] = {"domain": domain}
        logger.debug(f"Initialized ResultBuilder with domain: {domain}")

    def add_data(self, data: Dict[str, Any]):
        for key, value in data.items():
            if key in self.result and isinstance(self.result[key], list):
                # aggregate scan data from multiple sources (HTTPX, Nmap ..)
                self.result[key] = list(set(self.result[key] + value))
            else:
                self.result[key] = value
        return self

    def build(self) -> ScanResult:
        """
        Returns a validated ScanResult.
        """
        final_result = ScanResult(**self.result)
        logger.debug(f"Built final ScanResult: {final_result}")
        return final_result
