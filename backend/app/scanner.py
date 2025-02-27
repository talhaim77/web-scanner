import subprocess
import json
import shlex
from typing import Dict, Any
from fastapi.concurrency import run_in_threadpool
from app_logger import logger

class HTTPXScanner:
    """
    A Scanner class responsible for executing HTTPX CLI command
    and parsing the output to extract relevant metadata.
    """

    @staticmethod
    async def run_scan(domain: str) -> Dict[str, Any]:
        """
        Runs HTTPX CLI and yields parsed JSON objects line-by-line.
        """
        cmd = f"httpx -u {domain} -json -title -status-code -tech-detect -cname -ip -server -fr"
        logger.info(f"Starting HTTPX scan for {domain}")
        logger.debug(f"Constructed command: {cmd}")

        try:
            process = await run_in_threadpool(
                subprocess.run,
                shlex.split(cmd),
                capture_output=True,
                text=True,
                check=True,
            )
            logger.info(f"HTTPX scan completed for {domain}")
        except subprocess.CalledProcessError as e:
            logger.error(f"HTTPX scan failed for '{domain}': {str(e)}")
            yield {"error": f"HTTPX scan failed for '{domain}'", "details": str(e)}
            return

        for line in process.stdout.strip().split("\n"):
            if line.strip():
                try:
                    parsed_data = json.loads(line)
                    logger.debug(f"Parsed output: {parsed_data}")
                    yield parsed_data
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse line: {line}")
                    yield {"error": "Failed to parse line", "line": line}



