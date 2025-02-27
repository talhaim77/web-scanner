import logging
from config import configure_logging
from fastapi import APIRouter, HTTPException
from models import ScanResult
from utils.validators import is_valid_domain, check_domain_exists
from extractor import HTTPXExtractor
from builder import ResultBuilder
from scanner import HTTPXScanner

configure_logging()
logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/scan", response_model=ScanResult)
async def scan_website(domain: str):
    """
    API endpoint to scan a website and return metadata.
    """
    if not is_valid_domain(domain) or not check_domain_exists(domain):
        logger.warning(f"Invalid domain format received: {domain}")
        raise HTTPException(status_code=400, detail="Invalid domain format.")

    logger.info(f"Starting scan for domain: {domain}")

    extractor = HTTPXExtractor()
    builder = ResultBuilder(domain=domain)

    try:
        raw_data = await HTTPXScanner.run_scan(domain)
        if "error" in raw_data:
            logger.error(f"Error scanning {domain}: {raw_data}")
            raise HTTPException(status_code=500, detail=raw_data["error"])

        extracted = extractor.extract(raw_data)
        builder.add_data(extracted)
        logger.info(f"Scan completed for {domain}.")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(f"Unexpected error during scan of {domain}, {e}")
        raise HTTPException(status_code=500, detail=f"Scanning failed")

    return builder.build()