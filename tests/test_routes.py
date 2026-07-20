from app import create_app
from services.cache import write_cache
import pytest


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "CACHE_FILE": tmp_path / "cves.json"})
    write_cache(
        app.config["CACHE_FILE"],
        [
            {
                "id": "CVE-2026-0001",
                "description": "Safe test record",
                "published": "2026-01-01T00:00:00Z",
                "last_modified": None,
                "score": 9.8,
                "severity": "CRITICAL",
                "cvss_version": "3.1",
                "weaknesses": [],
                "nvd_url": "https://nvd.nist.gov/vuln/detail/CVE-2026-0001",
                "known_exploited": False,
                "kev_details": None,
            }
        ],
    )
    return app.test_client()


@pytest.mark.parametrize("path", ["/", "/owasp", "/cves", "/about", "/health"])
def test_routes_load(client, path):
    assert client.get(path).status_code == 200


def test_api_filters_and_validates(client):
    assert len(client.get("/api/cves?severity=CRITICAL").get_json()["cves"]) == 1
    assert client.get("/api/cves?severity=NOPE").status_code == 400


def test_security_header(client):
    assert "Content-Security-Policy" in client.get("/").headers
