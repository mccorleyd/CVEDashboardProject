from __future__ import annotations
from typing import Any


def first_english(items: list[dict[str, Any]], key: str = "value") -> str | None:
    for item in items:
        if item.get("lang") == "en" and item.get(key):
            return item[key]
    return items[0].get(key) if items else None


def normalise_cve(item: dict[str, Any]) -> dict[str, Any]:
    cve = item.get("cve", item)
    metrics = cve.get("metrics", {})
    metric = next(
        (
            metrics[key][0]
            for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2")
            if metrics.get(key)
        ),
        {},
    )
    cvss = metric.get("cvssData", {})
    score = cvss.get("baseScore")
    weaknesses = sorted(
        {
            d.get("value")
            for weakness in cve.get("weaknesses", [])
            for d in weakness.get("description", [])
            if d.get("value", "").startswith("CWE-")
        }
    )
    identifier = cve.get("id", "Unknown CVE")
    return {
        "id": identifier,
        "description": first_english(cve.get("descriptions", []))
        or "No English description supplied.",
        "published": cve.get("published"),
        "last_modified": cve.get("lastModified"),
        "score": score,
        "severity": cvss.get("baseSeverity")
        or metric.get("baseSeverity")
        or "UNASSIGNED",
        "cvss_version": cvss.get("version"),
        "weaknesses": weaknesses,
        "nvd_url": f"https://nvd.nist.gov/vuln/detail/{identifier}",
        "known_exploited": False,
        "kev_details": None,
    }


def normalise_response(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [normalise_cve(item) for item in payload.get("vulnerabilities", [])]
