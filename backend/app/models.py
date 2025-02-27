from pydantic import BaseModel
from typing import List, Optional


class ScanResult(BaseModel):
    domain: str
    related_ips: List[str] = []
    webpage_title: Optional[str] = None
    status_code: Optional[int] = None
    webserver: Optional[str] = None
    technologies: List[str] = []
    cnames: List[str] = []
