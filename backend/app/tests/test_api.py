import json

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

with open("tests/mock_scan_data.json", "r") as file:
    MOCK_SCAN_DATA = json.load(file)


@pytest.fixture
def fake_scan(monkeypatch):
    """Fixture to mock scanner HTTPXScanner.run_scan response."""
    from scanner import HTTPXScanner
    async def fake_run_scan(domain: str):
        """Mock response for a scan request."""
        yield MOCK_SCAN_DATA

    monkeypatch.setattr("scanner.HTTPXScanner.run_scan", fake_run_scan)


def test_api_scan_valid_domain(fake_scan):
    response = client.get("/api/scan?domain=netflix.com")
    assert response.status_code == 200
    data = response.json()

    # Expected Data
    expected_ips = set(MOCK_SCAN_DATA["a"])
    expected_technologies = set(MOCK_SCAN_DATA["tech"])

    assert data["domain"] == MOCK_SCAN_DATA["input"]
    assert set(data["related_ips"]) == expected_ips
    assert data["webpage_title"] == MOCK_SCAN_DATA["title"]
    assert data["status_code"] == MOCK_SCAN_DATA["status_code"]
    assert data["webserver"] == MOCK_SCAN_DATA["webserver"]
    assert set(data["technologies"]) == expected_technologies
    assert data["cnames"] == []  # Expect empty cnames
