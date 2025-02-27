import logging

from fastapi import APIRouter, HTTPException

from models import ScanResult

from utils.validators import is_valid_domain

from extractor import HTTPXExtractor

from builder import ResultBuilder

from scanner import HTTPXScanner

router = APIRouter()

logger = logging.getLogger("uvicorn")

@router.get("/api/scan", response_model=ScanResult)
async def scan_website(domain: str):
    """
    API endpoint to scan a website and return metadata.
    """
    if not is_valid_domain(domain):
        logger.warning(f"Invalid domain format received: {domain}")
        raise HTTPException(status_code=400, detail="Invalid domain format.")

    logger.info(f"Starting scan for domain: {domain}")

    extractor = HTTPXExtractor()
    builder = ResultBuilder(domain=domain)
    errors = []

    try:
        async for raw_data in HTTPXScanner.run_scan(domain):
            if "error" in raw_data:
                errors.append(raw_data)
                logger.error(f"Error scanning {domain}: {raw_data}")
                continue

            extracted = extractor.extract(raw_data)
            builder.add_data(extracted)

        logger.info(f"Scan completed for {domain}. Errors encountered: {len(errors)}")

    except Exception as e:
        logger.exception(f"Unexpected error during scan of {domain}")
        raise HTTPException(status_code=500, detail=f"Scanning failed: {e}")

    if errors:
        logger.warning(f"Scan for {domain} completed with {len(errors)} errors.")
        raise HTTPException(status_code=500, detail="One or more errors occurred during scanning.")

    return builder.build()