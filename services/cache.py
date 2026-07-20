from __future__ import annotations
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def read_cache(path: Path, ttl_seconds: int) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        fetched_at = datetime.fromisoformat(payload["fetched_at"])
        age = (datetime.now(UTC) - fetched_at).total_seconds()
        payload["is_fresh"] = age <= ttl_seconds
        payload["is_stale"] = not payload["is_fresh"]
        return payload
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return None


def write_cache(path: Path, cves: list[dict[str, Any]]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"fetched_at": datetime.now(UTC).isoformat(), "cves": cves}
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    temporary.replace(path)  # Atomic replacement avoids a half-written cache.
    payload.update({"is_fresh": True, "is_stale": False})
    return payload
