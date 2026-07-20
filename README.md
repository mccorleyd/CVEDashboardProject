# CyberScope: OWASP and CVE Security Dashboard

A classroom-ready reference app and guided UK Digital T Level project. It teaches students to build, test, secure and deploy a small Flask dashboard rather than copy an unexplained finished solution.

> Screenshot placeholder: add a desktop dashboard screenshot here after local run.
> Screenshot placeholder: add a mobile CVE explorer screenshot here after accessibility testing.

## Plan, tree, decisions and limits
**Plan:** configure safely → build Flask pages → model local OWASP data → call/normalise/cache NVD → filter safely in the browser → test/security review → deploy. **Tree:** `app.py`, `services/`, `data/`, `templates/`, `static/`, `tests/`, `scripts/`, `deployment/`, and course documents at the repository root. **Decisions:** Flask/Jinja keeps the first backend readable; file cache demonstrates persistence without a database; NVD data is normalised before templates; OWASP is local, curated JSON; CISA enrichment is best-effort. **Limits:** data is a small recent window, not an asset inventory or risk engine; CISA absence is not proof of no exploitation; a private IP cannot normally obtain a trusted public HTTPS certificate.

## Features and architecture
`Browser → Nginx → Gunicorn → Flask → NVD/CISA or local cache`. Routes: `/`, `/owasp`, `/cves`, `/cves/<id>`, `/about`, `/api/cves?severity=HIGH`, `/health`. CVE pages search/filter client-side using `textContent`, never unsafe HTML insertion. Cache writes atomically and falls back to stale data on NVD failure.

## Quick local setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env  # set values locally; do not commit it
pytest -q
python app.py
```
Visit `http://127.0.0.1:5000`. The development server is for local learning only; use Gunicorn behind Nginx in production.

## Configuration and sources
`NVD_API_KEY` is optional, `CACHE_TTL_SECONDS` defaults to 1800, and `ENABLE_CISA_KEV=true` controls optional enrichment. NVD API 2.0: <https://nvd.nist.gov/developers/vulnerabilities>. CISA KEV JSON: <https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json>. OWASP source: <https://owasp.org/www-project-top-ten/>. Source-check record is 2026-07-20; the build environment could not access those sites, so a mentor **must verify the current edition/URLs before delivery** and update the local dataset if needed. “This product uses the NVD API but is not endorsed or certified by the NVD.”

## Security, deployment and limitations
Headers, input validation, escaping, non-root systemd service, localhost Gunicorn, Nginx request limit, no committed secrets, and UFW guidance are included. Read [SECURITY_REVIEW.md](SECURITY_REVIEW.md), [TROUBLESHOOTING.md](TROUBLESHOOTING.md), and [deployment/DEPLOYMENT.md](deployment/DEPLOYMENT.md). Run `ruff check .` and `pytest -q`; live data is deliberately not a test dependency.
