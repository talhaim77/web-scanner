import logging
import subprocess
import json
from typing import Dict, Any
from fastapi.concurrency import run_in_threadpool
from config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

FLAGS = [
    "-json",
    "-title",
    "-status-code",
    "-tech-detect",
    "-cname",
    "-ip",
    "-server",
    "-fr",
]


class HTTPXScanner:
    """
    A Scanner class responsible for executing HTTPX CLI command
    and parsing the output to extract relevant metadata.
    """

    @staticmethod
    async def run_scan(domain: str) -> Dict[str, Any]:
        """
        Executes an HTTPX scan on the provided domain and returns the parsed JSON output.

        Parameters:
            domain (str): The domain to scan.

        Returns:
            Dict[str, Any]: The parsed JSON output from the HTTPX scan or an error dict.
        """
        cmd = ["httpx", "-u", domain] + FLAGS
        logger.info(f"Starting HTTPX scan for {domain}")
        logger.debug(f"Constructed command: {cmd}")
        try:
            process = await run_in_threadpool(
                subprocess.run,
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            logger.info(f"HTTPX scan completed for {domain}")
        except subprocess.TimeoutExpired as te:
            logger.error(f"HTTPX scan timed out for '{domain}': {str(te)}")
            return {"error": f"HTTPX scan timed out for '{domain}'", "details": str(te)}
        except subprocess.CalledProcessError as e:
            logger.error(f"HTTPX scan failed for '{domain}': {str(e)}")
            return {"error": f"HTTPX scan failed for '{domain}'", "details": str(e)}

        output = process.stdout
        logger.debug(f"HTTPX scan output: {output}, type: {type(output)}")
        if not output:
            logger.error(
                f"No output returned for domain {domain}. Domain might not be found."
            )
            return {
                "error": f"No output returned for domain {domain}. Domain might not be found."
            }

        try:
            parsed_data = json.loads(output)
            logger.debug(f"Json parsed output: {parsed_data}")
            return parsed_data
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse output: {output}")
            return {"error": "Failed to parse output", "output": output}
