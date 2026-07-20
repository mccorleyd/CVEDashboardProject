import json
from pathlib import Path
from services.normalisers import normalise_response

FIXTURES = Path(__file__).parent / "fixtures"


def test_normalises_expected_values():
    cve = normalise_response(json.loads((FIXTURES / "nvd_sample.json").read_text()))[0]
    assert (
        cve["id"] == "CVE-2026-0001"
        and cve["score"] == 9.8
        and cve["weaknesses"] == ["CWE-79"]
    )


def test_missing_values_are_safe():
    cve = normalise_response(json.loads((FIXTURES / "nvd_sample.json").read_text()))[1]
    assert (
        cve["score"] is None
        and cve["description"] == "No English description supplied."
        and cve["weaknesses"] == []
    )
