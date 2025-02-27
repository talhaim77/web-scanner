import pytest
from extractor import HTTPXExtractor

def test_httpx_extractor():
    # Sample raw data based on your provided JSON
    raw_data = {
        "timestamp": "2025-02-27T12:17:54.772777124Z",
        "cdn_name": "cloudflare",
        "cdn_type": "waf",
        "port": "443",
        "url": "https://mailtrap.io",
        "input": "mailtrap.io",
        "title": "Mailtrap: Email Delivery Platform",
        "scheme": "https",
        "webserver": "cloudflare",
        "content_type": "text/html",
        "method": "GET",
        "host": "172.67.5.169",
        "path": "/",
        "time": "562.76937ms",
        "a": ["104.22.7.198", "104.22.6.198", "172.67.5.169"],
        "aaaa": [
            "2606:4700:10::ac43:5a9",
            "2606:4700:10::6816:7c6",
            "2606:4700:10::6816:6c6"
        ],
        "tech": [
            "Cloudflare",
            "HTTP/3",
            "MySQL",
            "PHP",
            "Site Kit:1.111.1",
            "WP Rocket",
            "WordPress"
        ],
        "words": 76441,
        "lines": 2536,
        "status_code": 200,
        "content_length": 278095,
        "failed": False,
        "cdn": True,
        "knowledgebase": {"PageType": "other", "pHash": 0},
        "resolvers": ["1.1.1.1:53", "1.0.0.1:53"]
    }

    extractor = HTTPXExtractor()
    extracted = extractor.extract(raw_data)

    # Expected values
    expected_domain = "mailtrap.io"
    expected_related_ips = {
        "104.22.7.198", "104.22.6.198", "172.67.5.169",
    }
    expected_title = "Mailtrap: Email Delivery Platform"
    expected_status_code = 200
    expected_webserver = "cloudflare"
    expected_technologies = [
        "Cloudflare", "HTTP/3", "MySQL", "PHP",
        "Site Kit:1.111.1", "WP Rocket", "WordPress"
    ]
    expected_cnames = []

    assert extracted["domain"] == expected_domain
    assert set(extracted["related_ips"]) == expected_related_ips
    assert extracted["webpage_title"] == expected_title
    assert extracted["status_code"] == expected_status_code
    assert extracted["webserver"] == expected_webserver
    assert extracted["technologies"] == expected_technologies
    assert extracted["cnames"] == expected_cnames
