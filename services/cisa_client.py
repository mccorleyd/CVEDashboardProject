from __future__ import annotations
import logging
import requests

LOG = logging.getLogger(__name__)
KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"


def enrich_with_kev(cves: list[dict], timeout: int) -> list[dict]:
    try:
        catalogue = (
            requests.get(KEV_URL, timeout=timeout).json().get("vulnerabilities", [])
        )
        by_id = {item.get("cveID"): item for item in catalogue}
        for cve in cves:
            if details := by_id.get(cve["id"]):
                cve.update(
                    known_exploited=True,
                    kev_details={
                        "vendor_project": details.get("vendorProject"),
                        "product": details.get("product"),
                        "due_date": details.get("dueDate"),
                    },
                )
    except (requests.RequestException, ValueError) as error:
        LOG.warning("CISA KEV enrichment unavailable: %s", error)
    return cves
