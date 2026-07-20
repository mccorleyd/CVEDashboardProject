from __future__ import annotations
import logging
from datetime import UTC, datetime, timedelta
import requests
from .normalisers import normalise_response

LOG = logging.getLogger(__name__)
NVD_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


class NvdError(RuntimeError):
    pass


def fetch_recent_cves(
    api_key: str | None, timeout: int, results_per_page: int
) -> list[dict]:
    headers = {"apiKey": api_key} if api_key else {}
    # A one-day window keeps the demonstration request manageable; startIndex enables pagination later.
    start = (datetime.now(UTC) - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S.000")
    end = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.000")
    try:
        response = requests.get(
            NVD_URL,
            params={
                "pubStartDate": start,
                "pubEndDate": end,
                "resultsPerPage": results_per_page,
                "startIndex": 0,
            },
            headers=headers,
            timeout=timeout,
        )
        if response.status_code == 429:
            raise NvdError(
                "NVD is rate limiting requests; try again after the cache period."
            )
        response.raise_for_status()
        return normalise_response(response.json())
    except (requests.RequestException, ValueError) as error:
        LOG.warning("NVD request failed: %s", error)
        raise NvdError("NVD data could not be refreshed.") from error
