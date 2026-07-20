"""Configuration is read once when the Flask app starts."""

from __future__ import annotations
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def positive_int(name: str, default: int) -> int:
    try:
        value = int(os.environ.get(name, default))
        return value if value > 0 else default
    except ValueError:
        return default


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "development-only-change-me")
    CACHE_TTL_SECONDS = positive_int("CACHE_TTL_SECONDS", 1800)
    CVE_RESULTS_PER_PAGE = min(50, positive_int("CVE_RESULTS_PER_PAGE", 20))
    REQUEST_TIMEOUT_SECONDS = positive_int("REQUEST_TIMEOUT_SECONDS", 15)
    NVD_API_KEY = os.environ.get("NVD_API_KEY")
    ENABLE_CISA_KEV = os.environ.get("ENABLE_CISA_KEV", "true").lower() == "true"
    CACHE_FILE = Path(
        os.environ.get("CACHE_FILE", BASE_DIR / "instance/cache/cves.json")
    )
