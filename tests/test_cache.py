from app import create_app
from services.cache import write_cache
from services.nvd_client import NvdError


def test_stale_cache_fallback(tmp_path, monkeypatch):
    app = create_app(
        {"TESTING": True, "CACHE_FILE": tmp_path / "c.json", "CACHE_TTL_SECONDS": 1}
    )
    write_cache(app.config["CACHE_FILE"], [])
    monkeypatch.setattr(
        "app.fetch_recent_cves",
        lambda *args: (_ for _ in ()).throw(NvdError("offline")),
    )
    # Make cache stale by setting TTL to zero only after the successful write.
    app.config["CACHE_TTL_SECONDS"] = 0
    response = app.test_client().get("/api/cves").get_json()
    assert response["stale"] and "older cached" in response["warning"]
