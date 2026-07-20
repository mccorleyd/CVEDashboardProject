from __future__ import annotations
import json
import logging
from flask import Flask, abort, jsonify, render_template, request
from config import BASE_DIR, Config
from services.cache import read_cache, write_cache
from services.cisa_client import enrich_with_kev
from services.nvd_client import NvdError, fetch_recent_cves

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)


def load_owasp() -> dict:
    return json.loads((BASE_DIR / "data/owasp_top_10.json").read_text(encoding="utf-8"))


def get_data(app: Flask) -> dict:
    cached = read_cache(app.config["CACHE_FILE"], app.config["CACHE_TTL_SECONDS"])
    if cached and cached["is_fresh"]:
        return {**cached, "warning": None, "source": "cache"}
    try:
        cves = fetch_recent_cves(
            app.config["NVD_API_KEY"],
            app.config["REQUEST_TIMEOUT_SECONDS"],
            app.config["CVE_RESULTS_PER_PAGE"],
        )
        if app.config["ENABLE_CISA_KEV"]:
            cves = enrich_with_kev(cves, app.config["REQUEST_TIMEOUT_SECONDS"])
        return {
            **write_cache(app.config["CACHE_FILE"], cves),
            "warning": None,
            "source": "live",
        }
    except NvdError as error:
        if cached:
            return {
                **cached,
                "warning": f"{error} Showing older cached data.",
                "source": "stale cache",
            }
        return {
            "cves": [],
            "fetched_at": None,
            "is_stale": False,
            "warning": f"{error} No cached data is available.",
            "source": "unavailable",
        }


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    @app.after_request
    def security_headers(response):
        response.headers.update(
            {
                "X-Content-Type-Options": "nosniff",
                "Referrer-Policy": "strict-origin-when-cross-origin",
                "Permissions-Policy": "geolocation=(), camera=(), microphone=()",
                "X-Frame-Options": "DENY",
                "Content-Security-Policy": "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; frame-ancestors 'none'; base-uri 'self'",
            }
        )
        return response

    @app.route("/")
    def index():
        data = get_data(app)
        cves = data["cves"]
        counts = {
            s: sum(c["severity"] == s for c in cves)
            for s in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "UNASSIGNED")
        }
        return render_template(
            "index.html",
            data=data,
            cves=sorted(cves, key=lambda x: x["published"] or "", reverse=True)[:6],
            counts=counts,
        )

    @app.route("/owasp")
    def owasp():
        return render_template("owasp.html", owasp=load_owasp())

    @app.route("/cves")
    def cves():
        return render_template("cves.html", data=get_data(app))

    @app.route("/cves/<cve_id>")
    def cve_detail(cve_id):
        if not cve_id.startswith("CVE-"):
            abort(404)
        cve = next((x for x in get_data(app)["cves"] if x["id"] == cve_id), None)
        if not cve:
            abort(404)
        return render_template("cve_detail.html", cve=cve)

    @app.route("/about")
    def about():
        return render_template("about.html", data=get_data(app), owasp=load_owasp())

    @app.route("/api/cves")
    def api_cves():
        severity = request.args.get("severity")
        if severity and severity not in {
            "CRITICAL",
            "HIGH",
            "MEDIUM",
            "LOW",
            "UNASSIGNED",
        }:
            return jsonify(error="Invalid severity."), 400
        data = get_data(app)
        cves = data["cves"]
        if severity:
            cves = [c for c in cves if c["severity"] == severity]
        return jsonify(
            cves=cves,
            fetched_at=data["fetched_at"],
            stale=data["is_stale"],
            warning=data["warning"],
        )

    @app.route("/health")
    def health():
        return jsonify(status="ok")

    @app.errorhandler(404)
    def missing(_):
        return render_template(
            "error.html", message="That page or CVE was not found."
        ), 404

    return app


app = create_app()
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
