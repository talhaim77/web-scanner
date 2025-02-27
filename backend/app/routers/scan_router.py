from fastapi import APIRouter, HTTPException

from app_logger import logger
from models import ScanResult

from utils.validators import is_valid_domain

from extractor import HTTPXExtractor

from builder import ResultBuilder

from scanner import HTTPXScanner

router = APIRouter()

@router.get("/api/scan", response_model=ScanResult)
async def scan_website(domain: str):
    """
    API endpoint to scan a website and return metadata.
    """
    if not is_valid_domain(domain):
        raise HTTPException(status_code=400, detail="Invalid domain format.")

    extractor = HTTPXExtractor()
    builder = ResultBuilder(domain=domain)
    error_occurred = False

    try:
        async for raw_data in HTTPXScanner.run_scan(domain):
            if "error" in raw_data:
                error_occurred = True
                logger.info(f"Error in {raw_data}")
                continue

            extracted = extractor.extract(raw_data)
            builder.add_data(extracted)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scanning failed: {e}")

    if error_occurred:
        raise HTTPException(status_code=500, detail="One or more errors occurred during scanning.")

    return builder.build()