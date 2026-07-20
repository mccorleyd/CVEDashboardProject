# Student workbook — CyberScope

## How to work
For each phase: **concept → mentor demo → guided task → checkpoint → reflection → extension**. Type the small marked changes yourself; starter files are provided. Use documentation, browser DevTools Network/Console, `journalctl`, and logs before asking AI. Keep a decision record: **Decision | options | choice | reason | trade-off | result after testing**.

### Fixed versus choice
Fixed: Flask, NVD, local OWASP JSON, safe output, tests, secure deployment. Choose: name/branding, accessible palette, OWASP cards/accordion/table/timeline, CVE card/table, metrics/prioritisation, one extension and a non-technical explanation.

## Phase 1 — Direction (short)
**Learn:** audience, CVE/CWE/CVSS and prioritisation. **Demo:** mentor compares score with KEV evidence. **Task/deliverable:** audience statement, sketch and decision record. **Check:** sketch shows title, metrics, filters. **Reflect:** why is CVSS not business risk? **Mistake:** treating KEV absence as safe. **Stretch:** interview a non-technical user. **Commit:** `plan dashboard`.

## Phase 2 — Ubuntu orientation (medium)
A cloud instance is a rented remote computer; public IP reaches it, private IP is internal. SSH uses a key pair; verify the host-key fingerprint with the provider. Connect: `ssh -i key.pem ubuntu@PUBLIC_IP`. Practise `pwd`, `ls -la`, `cd`, `mkdir`, `cp`, `mv`, `cat`, `less`, `nano`, `grep`, `tail`, `whoami`, `id`, `ps`, `ss -tulpn`, `systemctl`, `journalctl`, `curl`. **Challenge:** create `~/practice/a.txt`, copy/move it, print it, then remove the practice folder. **Check:** explain each command. **Reflect:** what does sudo change? **Commit:** `record server orientation`.

## Phase 3 — Setup and Git (medium)
`sudo apt update && sudo apt upgrade`; install `git python3-venv python3-pip curl`. Run `git init`, `git status`, `git add`, `git commit`, `git log --oneline`, `git diff`. `.gitignore` prevents `.env` and `.venv` entering history. Make a branch, merge a deliberate one-line conflict, use `git revert`, then tag `v1.0.0`. **Check:** history has meaningful commits. **Mistake:** adding `.env`. **Stretch:** remote GitHub repo. **Commit:** `initial structure`.

## Phase 4 — First pages (medium)
A route maps a URL to a Python function; Jinja renders HTML. Read `app.py` route and `base.html`. **Type:** add a sentence to the home template. **Experiment:** change `<h1>` then reload; inspect its HTML in DevTools. **Likely error:** `ModuleNotFoundError` means activate `.venv`. **Check:** `/` and `/health` work. **Reflect:** why not expose debug Flask publicly? **Commit:** `first flask pages`.

## Phase 5 — OWASP data (medium)
Read `data/owasp_top_10.json`: titles are OWASP-summarised; explanations/examples are teaching text. **Task:** choose cards (reference), accordion, detail-table or timeline and improve one explanation in your own words. **Check:** all categories and official links render. **Experiment:** edit a JSON value; invalid comma gives a JSON decode error. **Extension:** update process: verify official release, update edition/categories/URLs/CWEs, peer-review, test, commit. **Commit:** `display owasp data`.

## Phase 6 — APIs (substantial)
An endpoint is a URL; `GET` reads data; headers carry metadata; JSON is nested lists/dictionaries. Run `curl -i 'https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=1'` (or inspect `tests/fixtures/nvd_sample.json` offline). Locate ID, description, published date, score, severity. Read `nvd_client.py`: `params`, optional header, `timeout`, `raise_for_status`. **Type:** change only `resultsPerPage` in a local experiment. **Failures:** 429 = wait/use cache; 500 = upstream issue; timeout = network/slow service; invalid JSON = do not trust it. **Check:** explain status codes. **Commit:** `nvd api client`.

## Phase 7 — Normalise, cache and present (substantial)
Upstream JSON is complex, so `normalise_cve` produces a small internal model. Cache means reuse a recent successful response: fresh is within TTL; stale is older but useful during failure. `write_cache` writes a temporary file then replaces it. **Task:** trace request from page to cache/API. **Experiment:** set a very short TTL and stop network access; observe stale warning. **Check:** no key in cache. **Commit:** `normalise and cache cves`.

## Phase 8 — UX (medium)
Read `dashboard.js`: it uses `textContent`, so external descriptions are displayed as text rather than interpreted as HTML. **Task:** test text, severity, minimum score, KEV, sort and clear; choose cards/table. **Check:** keyboard reaches every control and empty state appears. **Mistake:** relying only on colour. **Stretch:** dark mode. **Commit:** `add explorer filters`.

## Phase 9 — Tests and review (substantial)
A test is repeatable evidence. Arrange data, Act, Assert outcome. Unit tests test one function; route tests test joined pieces; fixtures are safe saved data; mocks simulate failures. Run `pytest -q` and `ruff check .`. Complete [SECURITY_REVIEW.md](SECURITY_REVIEW.md) and manual plan in [TROUBLESHOOTING.md](TROUBLESHOOTING.md). **Check:** tests never call live NVD. **Commit:** `test and security review`.

## Phase 10 — Deploy/evaluate (substantial)
Follow [deployment/DEPLOYMENT.md](deployment/DEPLOYMENT.md). **Check:** Nginx → Gunicorn → Flask works after logout/reboot; `/health` works; evidence screenshots/log snippets are saved. **Reflect:** one diagnosed problem and next feature. **Commit/tag:** `deploy v1` / `v1.0.0`.

## Extensions (easy → harder)
Each must have a short design/test record: **concept, prerequisites, approach, risks, acceptance criteria.** 1 dark preference (localStorage; contrast; survives reload); 2 pagination (arrays; correct pages); 3 clickable bars (events; filter changes); 4 Chart.js (library; CSP/change control); 5 timer refresh (scheduling; avoid rate limits); 6 NVD keyword query (query validation; no huge queries); 7 published/modified comparison (dates; labels correct); 8 KEV enrichment (HTTP failures; badges); 9 CSV export (escaping; downloads); 10 SQLite watchlist (database; no secrets); 11 server filters (validation; tests); 12 another endpoint (API design; docs); 13 private basic auth (credentials; HTTPS); 14 CI (GitHub Actions; tests); 15 containers **after** deployment (isolation; complexity); 16 uptime monitor (observability; false alarms); 17 JSON logs (structured events; no secrets); 18 SBOM (dependencies; accuracy); 19 dependency scanning (advisories; triage); 20 accessibility audit (WCAG; evidence).

## Responsible AI and AI log
AI may explain errors/syntax, suggest tests, review a small function, produce fixture ideas, compare approaches, or improve prose. Do not ask it for the whole assessed project, share secrets, run unexplained commands, skip testing, assume security advice is correct, or hide use where disclosure is required. Log: **date | question | tool | useful response | verification | changed | learned**.

## Team option and final demo
For 2–3: backend/API; frontend/accessibility; infrastructure/testing/docs. Every person contributes code, test, documentation and deployment. Board: **Backlog | Ready | In progress | Review | Done**. Demo: dashboard, OWASP, live/cached CVEs, filters, failure, architecture, Git, tests, controls, a choice, diagnosis, next feature. Strong answer: “KEV is exploitation evidence; CVSS is technical severity; we still check our assets and exposure.”
