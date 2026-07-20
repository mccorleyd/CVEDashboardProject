# Your Vulnerability Dashboard

Vulnerability Dashboard is a complete UK Digital T Level classroom project: a readable Flask reference implementation plus a guided workbook designed for a broad range of learners. Students learn to orient themselves on Ubuntu, write core Python, build HTML/CSS/JavaScript pages from scratch, use Git, understand JSON/APIs, normalise/cache vulnerability data, test failure paths, review security and deploy with Gunicorn, systemd and Nginx.

## Start with the workbook
Read [STUDENT_GUIDE.md](STUDENT_GUIDE.md) from Lesson 1 onwards. It is a single linear read — worked examples and practice labs sit next to the lesson that needs them rather than in separate appendices. It contains 13 lessons, a reusable invented practice dataset, a command reference, guided build tasks (including authoring a brand-new Flask route and a brand-new JSON file from scratch), controlled experiments, errors, checkpoints, 14 challenge cards, responsible-AI guidance, a paired merge-conflict exercise, a final demo and 20 assessed extensions. [TEACHING_NOTES.md](TEACHING_NOTES.md) is optional delivery support; students can complete the workbook independently.

## Architecture and routes

```text
Browser → Nginx → Gunicorn → Flask → file cache → NVD API / optional CISA KEV API
```

Routes: `/`, `/owasp`, `/cves`, `/cves/<CVE-ID>`, `/about`, `/api/cves?severity=HIGH`, `/health`. The reference uses local curated OWASP JSON, normalises NVD records before display, uses atomic file writes, displays stale-cache warnings, validates local query input, and uses Jinja escaping/JavaScript `textContent` for external text.

## Quick local setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
pytest -q
python app.py
```
Open `http://127.0.0.1:5000`. The Flask development server is local-learning only; production uses Gunicorn behind Nginx. See [deployment/DEPLOYMENT.md](deployment/DEPLOYMENT.md) for the full Ubuntu journey.

## Configuration and sources
`NVD_API_KEY` is optional. `CACHE_TTL_SECONDS` defaults to 1800 seconds. `ENABLE_CISA_KEV=true` controls enrichment. No real `.env` file or key belongs in Git. Sources: [NVD API 2.0](https://nvd.nist.gov/developers/vulnerabilities), [CISA KEV JSON](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json), and [OWASP Top 10](https://owasp.org/www-project-top-ten/). “This product uses the NVD API but is not endorsed or certified by the NVD.”

The source-check record is 2026-07-20. The build environment could not connect to official sites, so the included local OWASP teaching dataset carries a clear maintenance warning. Before use, verify the current released OWASP edition and current official API URLs before classroom delivery, update/review the data if necessary, validate JSON, test `/owasp`, and commit the update.

## Security, quality and known limits
Security controls cover environment variables, non-root service operation, localhost Gunicorn, Nginx request limits, UFW/SSH guidance, validation, output encoding, timeout/error handling and security headers. Complete [SECURITY_REVIEW.md](SECURITY_REVIEW.md) and use [TROUBLESHOOTING.md](TROUBLESHOOTING.md). Run `pytest -q`, `ruff check .`, and `./scripts/check_setup.sh`.

This is a learning dashboard, not an asset inventory, scanner, remediation tool or risk decision engine. It fetches a small recent NVD window. CVSS does not represent complete organisational risk; CISA KEV absence does not show that a vulnerability is not exploited. File cache is deliberately simple; a multi-server production deployment would use managed shared storage.
