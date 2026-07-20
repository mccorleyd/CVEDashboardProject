# Vulnerability Dashboard student workbook

**Audience:** Digital T Level students building and deploying a security dashboard.
**Project outcome:** a small, accessible security dashboard running on an Ubuntu server.
**How long:** a guided week of lessons plus optional extensions. Plan the lessons across at least five study sessions; do not rush server-security steps.

> **Important safety rule:** never paste an API key, private SSH key, password or a server IP that is not public into chat, screenshots, Git, or an AI tool. Never run a command on the cloud server unless you can say what it will do and how to check it worked.

---

## 0. Start here: the map of the project

### What you are building
Vulnerability Dashboard is a website which shows two kinds of security information:

* **OWASP Top 10** — a locally stored, student-friendly guide to common web application security risks.
* **CVE records** — recent public vulnerability records from NIST's NVD API, reduced to a short, safe-to-display format.

It is not a scanner and it does not decide whether an organisation is safe. A CVSS score is a technical severity score. CISA KEV membership is evidence that a vulnerability has been exploited. A security team still needs to check whether it uses the affected product, whether it is exposed, and whether a fix is available.

### The request journey

```text
Your browser
    │ HTTP/HTTPS request
    ▼
Nginx (public web server, later)
    ▼
Gunicorn (runs Python workers, later)
    ▼
Flask application ──► local cache file ──► NVD API / optional CISA KEV API
    ▼
HTML, CSS and JavaScript sent back to your browser
```

### Rules, choices and evidence

|Fixed core requirements|Your choices|
|---|---|
|Flask, NVD API, local OWASP JSON, safe output, tests, non-root deployment|Project name/logo text, accessible colour palette, OWASP layout, CVE card/table layout, summary metrics, priority order, one extension|

Keep a folder named `evidence` outside Git or a private classroom drive. Save command output, screenshots, test results, decision records and feedback there.

### Decision record template

```text
Decision:
Options considered:
Choice:
Reason:
Trade-off or downside:
What I tested:
Result after testing:
Date and initials:
```

### Learning routine for every lesson
1. Read **Why this matters** first.
2. Read the worked example before starting the task.
3. Complete each numbered task. Type commands; do not blindly paste a whole lesson.
4. Stop at the **checkpoint** and collect evidence.
5. Answer the **reflection** in your own words.
6. Try the **stretch** only when the core works.

### Help ladder
Before asking a person or AI, spend ten minutes on these steps: (1) read the exact error, (2) check the spelling and current folder, (3) use `git diff`, browser DevTools or a log, (4) search official documentation using the error wording, (5) write down what you tried. Ask for an explanation, not a complete replacement solution.

---

# Lesson 1 — Understand the problem and plan your dashboard
**Effort:** short. **Suggested Git checkpoint:** `plan dashboard direction`.

## Learning objectives
By the end, you can explain CVE, CWE, CVSS, OWASP and CISA KEV in simple language; identify the project audience; and make a justified design choice.

## Concept overview
A **CVE** is an identifier such as `CVE-2026-0001` for a publicly reported vulnerability. A **CWE** names a class of weakness, for example a type of input-handling mistake. **CVSS** gives a standard technical score, normally 0–10. It is useful, but it does not know your organisation's systems, data or controls. **OWASP** publishes application-security education. **CISA KEV** is a US catalogue of vulnerabilities known to be exploited; absence from the catalogue is *not* proof that no exploitation exists.

## Worked example — deciding what to look at first
Read the two **invented** records below. They are teaching data, not real vulnerabilities and not instructions to attack anything.

|Question|Record A: CVE-2026-90001|Record B: CVE-2026-90002|
|---|---|---|
|CVSS severity|Critical, 9.8|High, 8.1|
|CISA KEV status|Not listed|Listed as known exploited|
|Product|Northstar Archive Server 4|BrightDesk Remote Support 7|
|Does the organisation use it?|No: asset list and software inventory show no installation|Yes: it is used on a public helpdesk server|
|Internet exposure|Not applicable|Public login page is reachable|
|Fix available?|Unknown|Vendor patch is available|
|First action|Record the result and confirm the inventory is current|Assign urgent investigation: confirm version, restrict exposure if appropriate, test/apply the vendor patch under change control|

A quick ranking by score alone would put Record A first because 9.8 is larger than 8.1. A security team instead uses several signals. Record B has a used product, public exposure, a known-exploited signal and a patch. It may therefore be investigated first. This is not an automatic rule: the team still checks its own systems, service importance, compensating controls and change window.

### Try the reasoning yourself
For each statement, decide whether it is **true**, **false**, or **not enough information**:

1. “Record A is harmless because the organisation does not use it.”
2. “Record B is definitely being exploited on this organisation's server.”
3. “A CVSS score tells us whether a patch will be easy to apply.”
4. “CISA KEV is a useful prioritisation signal.”

**Answers:** 1 is *not enough information*: the inventory might be incomplete, so record the check. 2 is *false*: KEV means exploitation is known in the wider world, not necessarily on this server. 3 is *false*: CVSS is not a change-management measure. 4 is *true*, but it must be combined with local context.

## Tasks
1. Write an audience statement: “This dashboard helps ___ decide ___ because ___.”
2. Draw the home page on paper. Include a title, four number cards, severity bars, a “look first” explanation, and a recent-CVE list.
3. Pick a name, font style and two main colours. Use an online contrast checker or browser DevTools to check text contrast. Do not use colour alone to mean “critical”.
4. Complete a decision record for your OWASP layout: cards, accordion, table/detail panel, or vertical timeline. The reference app uses cards; changing it is an extension after the core works.

## Checkpoint and reflection
Show the sketch and decision record. Explain: “Why might a high CVSS score not be first priority?”
**Common mistake:** saying KEV means every organisation is affected. It means there is exploitation evidence, not that your systems are vulnerable.

**Stretch:** write a 50-word explanation of Vulnerability Dashboard for a non-specialist school governor.

---

# Lesson 2 — Meet your Ubuntu cloud server
**Effort:** medium. **Suggested Git checkpoint:** `record server orientation`.

## Why this matters
A cloud instance is a remote virtual computer rented from a provider. You control it through a terminal. A **public IP address** can be reached from the internet; a **private IP address** is for internal networks. Treat the server like a real production system: use named users, record changes and avoid unnecessary exposure.

## New words
* **SSH (Secure Shell):** encrypted remote terminal connection.
* **Key pair:** a private key kept secret on your computer and a public key installed on the server.
* **Host key:** the server's identity fingerprint. Check it with the cloud-provider dashboard or trusted course record the first time.
* **user:** an account with its own files and permissions.
* **sudo:** “run this command with administrator privileges”. It is powerful, not a shortcut.

## First connection
Your cloud-provider dashboard or course setup record gives you a hostname or public IP, username and private-key file. In your own terminal, move to the folder containing the key. On Windows PowerShell, `cd` works too; on macOS/Linux use Terminal.

```bash
cd ~/Downloads
ssh -i vulnerability-dashboard-class.pem ubuntu@203.0.113.10
```

**What each part means:** `cd` changes folder; `-i` selects the identity/private-key file; `ubuntu@...` means “log in as ubuntu on this server”. The address above is documentation-only; use the address in your own setup record.

If asked whether to trust an unknown host key, **stop and compare the fingerprint with the cloud-provider dashboard or trusted setup record**. Do not accept a different fingerprint without investigation.

### Commands you will practise

|Command|Purpose|Example|What to look for|
|---|---|---|---|
|`pwd`|print current folder|`pwd`|Usually `/home/ubuntu`|
|`ls -la`|list files, including hidden ones|`ls -la`|`.` means current; `..` parent|
|`cd NAME`|enter a folder|`cd projects`|Prompt/folder changes|
|`cd ..`|go up one level|`cd ..`|Useful after a mistake|
|`mkdir NAME`|make a folder|`mkdir practice`|New folder appears in `ls`|
|`cp A B`|copy file|`cp notes.txt notes-copy.txt`|Both files exist|
|`mv A B`|move/rename|`mv notes-copy.txt old-notes.txt`|Old name disappears|
|`cat FILE`|print small file|`cat notes.txt`|Use only for short text|
|`less FILE`|read long file|`less /etc/ssh/sshd_config`|`q` quits|
|`nano FILE`|simple terminal editor|`nano notes.txt`|`Ctrl+O`, Enter saves; `Ctrl+X` exits|
|`grep TEXT FILE`|find text|`grep -n 'Port' /etc/ssh/sshd_config`|`-n` includes line numbers|
|`tail -n 30 FILE`|last lines of a file|`tail -n 30 /var/log/...`|Useful for new log entries|
|`whoami` / `id`|current user/permissions|`id`|Shows groups|
|`ps aux`|running processes|`ps aux | grep gunicorn`|A pipe sends output to grep|
|`ss -tulpn`|list listening network ports|`sudo ss -tulpn`|Check what is reachable|
|`systemctl`|manage services|`systemctl status nginx`|Does not edit files|
|`journalctl`|read service logs|`journalctl -u nginx -n 30`|`-u` selects a service|
|`curl`|make an HTTP request|`curl -I http://127.0.0.1`|`-I` asks for headers|

## Guided navigation challenge
1. Run `pwd`. Copy the output into evidence.
2. Run `mkdir -p ~/vulnerability-dashboard-practice/notes`. `-p` creates needed parent folders too.
3. Run `cd ~/vulnerability-dashboard-practice/notes`, then `pwd`. Explain why this works from any starting folder: `~` means your home folder.
4. Run `nano commands.txt`, type `I can navigate Linux.`, save and exit.
5. Run `cat commands.txt`; then copy and rename it: `cp commands.txt copy.txt` and `mv copy.txt moved.txt`.
6. Run `ls -la`, then `cd ..`, then `ls -la notes`.
7. Clean up only your practice folder: `rm -r ~/vulnerability-dashboard-practice`. `rm -r` permanently deletes a folder and its contents. Run `pwd` first and type the full path; never use it with a path you do not understand.

## Checkpoint
Run `whoami`, `id`, `ss -tulpn`, and `systemctl status ssh --no-pager`. A pager lets long output scroll; `--no-pager` prints it once. Explain which command tells you your current folder and which command tells you your identity.

**Likely errors:** `No such file or directory` usually means the folder/file spelling is wrong; use `pwd` and `ls`. `Permission denied` means your user cannot perform that action; do not automatically add `sudo`—ask why permission is needed.

---

# Lesson 3 — Secure the starting point
**Effort:** medium. **Suggested Git checkpoint:** `document basic server hardening`.

## Why this matters
A public server receives internet traffic. Least privilege means each user and service has only the access it needs. Do hardening one small reversible step at a time.

## Tasks with verify and undo steps
1. **Update the operating system.**
   ```bash
   sudo apt update
   sudo apt upgrade
   ```
   `apt update` downloads a list of available package versions. `apt upgrade` installs updates. Verify that it finishes without errors. Undoing package updates is not usually simple; take a provider snapshot first if your cloud-provider account provides it.
2. **Create the application account.**
   ```bash
   sudo adduser --system --group --home /srv/vulnerability-dashboard vulnerability-dashboard
   id vulnerability-dashboard
   ```
   This makes a non-login system user and group for the service. Verify its UID/group using `id`. If created in error before deployment, you can remove it with `sudo deluser --remove-home vulnerability-dashboard`.
3. **Review SSH before changing it.**
   ```bash
   sudo less /etc/ssh/sshd_config
   sudo sshd -t
   ```
   Look for `PasswordAuthentication` and `PermitRootLogin`. `sshd -t` checks syntax without applying changes. **Do not close the current session.** After checking the configuration and opening a second SSH terminal, open a second SSH terminal and confirm key login works before reloading SSH: `sudo systemctl reload ssh`.
4. **Set the firewall carefully.**
   ```bash
   sudo ufw allow OpenSSH
   sudo ufw status numbered
   sudo ufw enable
   sudo ufw status verbose
   ```
   UFW is Ubuntu's firewall tool. First allowing `OpenSSH` prevents locking yourself out. Verify rules and status. Undo a specific accidental rule with `sudo ufw delete NUMBER`, using the number shown; emergency undo is `sudo ufw disable`, and record the change.
5. **Inspect ports.** Run `sudo ss -tulpn`. At this stage, only services you expect should listen. Later, allow Nginx HTTP/HTTPS rather than opening Gunicorn's internal port.

## Reflection
Why is running Gunicorn as `root` a poor choice? What is the safe rollback if a new SSH setting stops the second connection?
**Stretch:** write a one-paragraph change record with purpose, command, verification and rollback for one firewall change.

---

# Lesson 4 — Install developer tools and start Git
**Effort:** medium. **Suggested Git checkpoint:** `initial project structure`.

## Concept overview
**Git** records snapshots (commits) of work. It is not a backup for passwords: `.gitignore` tells Git which local files, such as `.env`, must not be added. A **repository** is the folder Git tracks. A **virtual environment** (`venv`) is an isolated folder containing Python packages for one project.

## Install and check tools
```bash
sudo apt install -y git python3 python3-venv python3-pip curl
python3 --version
git --version
curl --version
```
`-y` confirms the package manager question automatically. Check that each version command prints a version. If it does not, copy the exact error into evidence.

## Get the project and create the environment
```bash
cd /srv
sudo git clone YOUR_REPOSITORY_URL vulnerability-dashboard
sudo chown -R "$USER":"$USER" /srv/vulnerability-dashboard
cd /srv/vulnerability-dashboard
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```
`source` runs the activation script in the current shell. Your prompt normally starts with `(.venv)`. It does not modify Python globally. Leave it later with `deactivate`. If `pip` installs but `python` cannot import Flask, check whether the prompt has `(.venv)`.

## Git guided tasks
```bash
git status
git add README.md
git commit -m "Explain project purpose"
git log --oneline
git diff
git switch -c improve-readme
# make one small documentation change
git add README.md && git commit -m "Clarify local setup"
git switch work
git merge improve-readme
```
`git status` answers “what changed?”; `git add` chooses changes for the next snapshot; `git commit -m` records them with an explanation; `git diff` shows unstaged changes. If your branch name is not `work`, run `git branch --show-current` and substitute it.

### Controlled merge-conflict exercise
In a pair, both edit the same single sentence differently in separate branches. Merge one branch, then merge the other. Git places conflict markers. Read both versions, keep the intended text, remove the markers, `git add`, and commit. To reverse a bad *committed* change without rewriting history: `git revert COMMIT_ID`. Release the final tested version: `git tag -a v1.0.0 -m "First classroom release"`.

**Never:** add `.env`, `*.pem`, downloaded keys or copied server secrets. Check `git status` before every `git add .`.

---

# Lesson 5 — Build and understand the first Flask pages
**Effort:** medium. **Suggested Git checkpoint:** `add first Flask pages`.

## What Flask, HTML and templates do
A web request has a **method** (for example GET), a **URL**, headers and a response. Flask maps a URL to a Python function called a **route**. The route calls a template. A Jinja template is HTML with safe placeholders such as `{{ name }}`. CSS controls appearance; JavaScript adds small browser behaviour.

## Run the reference application locally
```bash
source .venv/bin/activate
python app.py
```
Open `http://127.0.0.1:5000`. `127.0.0.1` means “this computer only”. Do **not** run Flask's development server on `0.0.0.0` on a public server. Stop it with `Ctrl+C`.

## Read before editing
In `app.py`, find `@app.route("/")`. The `@` line is a decorator: it tells Flask which URL should call the function below it. In `templates/base.html`, find `{% block content %}`; child pages fill that named area. In `templates/index.html`, `{{ data.fetched_at }}` inserts a value and Jinja escapes text by default.

## Guided small change
1. Open `templates/index.html` using `nano`.
2. Under the introductory paragraph, type one sentence explaining your chosen audience. This is **your code/text**, not starter code.
3. Save, refresh the browser, then use browser DevTools: right-click the sentence → Inspect.
4. Change one CSS colour in `static/css/styles.css`, refresh, and use the DevTools Elements/Styles panel to see the applied rule.
5. Run `curl -i http://127.0.0.1:5000/health`. Identify the `HTTP/` status line and JSON body.

**Experiment A:** change `/health` to a nonexistent URL in curl; notice `404`. **Experiment B:** deliberately remove a closing Jinja brace, reload, read the error locally, restore it immediately. Production visitors receive a generic error page, not a traceback.

**Likely errors:** `Address already in use` means another process owns port 5000; use `ss -tulpn | grep 5000` and stop only your process. `TemplateNotFound` usually means wrong filename/folder. A browser cache can hide CSS changes; hard refresh with Ctrl+Shift+R.

---

# Lesson 6 — Model OWASP Top 10 content
**Effort:** medium. **Suggested Git checkpoint:** `display OWASP teaching data`.

## Why local JSON?
JSON is a text data format using objects `{}` and lists `[]`. The project keeps OWASP material in `data/owasp_top_10.json`, rather than scraping a webpage every request. That makes lessons reliable and lets a maintainer review wording. The source file labels official summaries separately from student-friendly explanations.

## Read the data
Open it with `less data/owasp_top_10.json`. Find `edition`, `categories`, an `id`, `name`, `explanation`, `example`, `impact`, `prevention`, `url`, and `cwes`. A comma separates fields; strings require quotation marks. Run:
```bash
python -m json.tool data/owasp_top_10.json > /dev/null
echo $?
```
Exit code `0` means valid JSON. If invalid, Python prints a line/column. Go to that line and look for a missing comma, quote or bracket.

## Guided task
1. Visit `/owasp` and locate one category.
2. In the matching JSON item, improve **one** student explanation in plain English. Keep the meaning accurate and do not invent a claim about OWASP.
3. Refresh `/owasp`; check the card, link text and keyboard tab order.
4. Add a decision record explaining why you retained cards or chose a different layout.

### Maintenance process
Before a future update, read the official OWASP Top 10 project, record the date and edition, compare categories, update the local JSON and links, label any student-written text, validate JSON, test `/owasp`, ask another person to review, then commit with a clear message. Never scrape OWASP at runtime.

---

# Lesson 7 — Learn APIs with NVD fixtures and `curl`
**Effort:** substantial. **Suggested Git checkpoint:** `learn NVD API request`.

## API vocabulary
An **API** is an agreed way for programs to exchange information. An **endpoint** is an API URL. A **query parameter** adds a choice after `?`, for example `?resultsPerPage=1`. A **header** carries request metadata. A **status code** reports result: 200 successful, 400 invalid request, 401/403 access issue, 404 absent, 429 rate limit, 500 server fault. JSON can nest lists and dictionaries.

## Exercise A: make a small manual request
When network access is permitted, run:
```bash
curl -i 'https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=1'
```
`-i` includes response headers. Find the first `HTTP` status, `Content-Type`, then the JSON body. Do not repeatedly run it: unauthenticated NVD requests are rate limited. If the classroom network blocks it, use the saved fixture below—this is a valid offline learning route.

## Exercise B: inspect a saved response
```bash
python -m json.tool tests/fixtures/nvd_sample.json | less
```
Find `CVE-2026-0001`, the English `description`, `published`, `baseScore`, and `baseSeverity`. Notice that `vulnerabilities` is a list, then each item has a `cve` dictionary. `tests/fixtures` is controlled sample data, not live data.

## Exercise C: request from Python
Read `services/nvd_client.py`. The important starter code is:
```python
response = requests.get(NVD_URL, params=parameters, headers=headers, timeout=timeout)
response.raise_for_status()
payload = response.json()
```
`requests.get` sends HTTP GET. `params` becomes query parameters safely. `timeout` prevents waiting forever. `raise_for_status` turns bad HTTP status into an exception. `.json()` parses JSON. **Do not type an API key into this file.** The app reads `NVD_API_KEY` from an environment variable.

**Controlled experiments:** (1) in a scratch Python file, print `response.status_code` after a permitted one-record request; (2) set `timeout=0.001` only in a local experiment and observe error handling, then restore it.
**Likely errors:** 429 means wait and use cache, not a loop; invalid JSON should be handled as unavailable data; 500 is usually upstream; a timeout may be network or service delay.

---

# Lesson 8 — Normalise, cache and enrich CVEs
**Effort:** substantial. **Suggested Git checkpoint:** `normalise cache and enrich Cves`.

## Why a normalisation layer exists
NVD's full JSON is designed for many uses. Templates only need a small model. `services/normalisers.py` converts each record to `id`, `description`, dates, score, severity, CVSS version, CWEs, NVD URL and optional KEV details. It carefully handles missing English text, no score and no CWE. Do not pass an entire external response directly into templates.

## Read one function line-by-line
```python
metric = next((metrics[key][0] for key in (...) if metrics.get(key)), {})
score = cvss.get("baseScore")
```
`next(..., {})` takes the first available metric or safely uses an empty dictionary. `.get` returns `None` instead of crashing when a key is absent. This is starter code. Your task is to explain it in a comment or notebook, not rewrite it from memory.

## Cache concepts
A cache is a saved successful result. It improves speed and respects rate limits. `CACHE_TTL_SECONDS` decides how long data is **fresh** (default 30 minutes). After that, the app tries NVD. If NVD fails and old data exists, it shows **stale** cached data and a warning. `write_cache` writes a temporary file then replaces it so a crash does not leave half JSON. It never stores the API key. Production systems might use Redis/database because multiple servers need shared, managed storage.

## Guided tasks
1. Create local configuration without committing it: `cp .env.example .env`. Read the comments. Leave `NVD_API_KEY` blank; the app must work without it.
2. Populate a known cache from the fixture:
   ```bash
   python - <<'PY'
   import json
   from pathlib import Path
   from services.cache import write_cache
   from services.normalisers import normalise_response
   write_cache(Path('instance/cache/cves.json'), normalise_response(json.loads(Path('tests/fixtures/nvd_sample.json').read_text())))
   PY
   ```
   This is provided classroom setup code. Read it: it loads JSON, normalises it, then writes cache data.
3. Run the app and visit `/`, `/cves`, `/api/cves`. Confirm fixture data appears.
4. Set `CACHE_TTL_SECONDS=1` in your shell (`export CACHE_TTL_SECONDS=1`), restart the app, wait two seconds and disconnect/disable external access only on a non-production/local test environment. Observe the stale warning when upstream data cannot refresh. Restore the default by closing that terminal or `unset CACHE_TTL_SECONDS`.
5. Explain why the CISA client catches failures and still returns CVEs.

---

# Lesson 9 — Make the CVE explorer usable and safe
**Effort:** medium. **Suggested Git checkpoint:** `add search filters and accessible UX`.

## Browser filtering
The server supplies a normalised list. `static/js/dashboard.js` filters the list in the browser by search, severity, minimum score and KEV flag, then sorts it. This is suitable for a small teaching data set. Larger data needs pagination/server-side filtering.

### Critical security detail
API descriptions are external input. Inserting it with `innerHTML` can make the browser interpret markup. The reference creates elements and uses `textContent`, which displays data as text. Keep this behaviour. Jinja also escapes `{{ values }}` by default.

## Guided tasks
1. Open `/cves`. Search an identifier, choose each severity, set a minimum score, tick KEV-only, change sort and press Clear filters.
2. Use Tab, Shift+Tab, Enter and Space only. Can you open navigation, use every form control and read the result-count update?
3. Use responsive mode in DevTools (or shrink browser under 650px). Open and close Menu. Check text does not overlap and focus outline is visible.
4. Add one plain-English empty-state sentence or improve an accessible label. Test it with a deliberately non-matching search.
5. Inspect `dashboard.js` and identify the line using `textContent`. Explain why a description containing angle brackets is displayed, rather than run.

**Common mistakes:** hiding focus outlines; using red/green without words; changing `textContent` to `innerHTML`; assuming “not scored” means low risk.

---

# Lesson 10 — Test, debug and security-review
**Effort:** substantial. **Suggested Git checkpoint:** `test and security review`.

## What tests are
A test is repeatable evidence. **Arrange** creates inputs; **Act** calls code; **Assert** checks expected output. Unit tests check a small unit such as a normaliser. Route tests check Flask responses. Fixtures provide predictable data. Mocks replace a live dependency to simulate timeout/failure. Tests must not depend on a live public API because its data/network can change.

## Run and read tests
```bash
source .venv/bin/activate
pytest -q
ruff check .
```
`-q` means quieter output. `ruff` checks style and likely mistakes. Read `tests/test_normalisers.py`, then identify Arrange, Act and Assert. Read `tests/test_cache.py`: `monkeypatch` temporarily replaces the network function so failure is safe and repeatable.

## Guided test task
Add one test for `/api/cves?severity=HIGH` using the fixture/cache pattern in `test_routes.py`. First predict expected count, run the test, then make it pass. Do not call NVD from the test. Commit only when the full suite passes.

## Manual test record
For each item write expected/actual/evidence/fix commit: desktop, mobile, keyboard, search, each filter, empty result, stale cache, broken upstream data, broken link, DevTools Console, Nginx reload, app restart, and `/health`.

## Security self-review
Complete `SECURITY_REVIEW.md`. Check headers locally:
```bash
curl -I http://127.0.0.1:5000/
git status
git grep -n 'NVD_API_KEY'
```
The first checks response headers. The second checks accidental files. The third finds key *references*, not keys; verify no real value is tracked. Explain CSP, referrer policy, MIME sniffing protection, permissions policy and frame protection in your own words.

---

# Lesson 11 — Deploy with Gunicorn, systemd and Nginx
**Effort:** substantial. **Suggested Git checkpoint:** `deploy vulnerability dashboard securely`; **release tag:** `v1.0.0`.

Follow `deployment/DEPLOYMENT.md` in order. It is written so you can verify each step yourself. This workbook explains the why; that guide gives exact verified commands and rollback. Do not skip the second SSH connection/firewall checks.

## Production terms
* **Gunicorn:** production server that runs Flask worker processes; bind it to `127.0.0.1:8000`, not public internet.
* **systemd:** Ubuntu service manager. It starts Gunicorn after reboot and keeps logs.
* **Nginx:** public reverse proxy. It receives web traffic, serves as a controlled front door and forwards to Gunicorn.
* **UFW:** host firewall. Allow SSH and Nginx HTTP/HTTPS only.
* **HTTPS:** encryption between browser and Nginx. A public trusted certificate needs a valid domain pointing at the server; a bare private IP normally cannot receive one.

## Deployment checklist
1. Create the `vulnerability-dashboard` non-root service user and `/srv/vulnerability-dashboard` directory with correct ownership.
2. Clone the repository, create `/srv/vulnerability-dashboard/.venv`, install pinned requirements.
3. Put secrets only in `/etc/vulnerability-dashboard/vulnerability-dashboard.env`, owned root and readable by the service group; never in Git.
4. Test Gunicorn manually from a second terminal with `curl http://127.0.0.1:8000/health`.
5. Copy the provided systemd service, run `daemon-reload`, enable/start, inspect `systemctl status` and `journalctl -u vulnerability-dashboard`.
6. Copy Nginx configuration, set the real domain, run `sudo nginx -t` **before** reload, then reload and test public routes/static CSS.
7. Apply UFW Nginx rule after confirming SSH safety. Check `ss -tulpn`.
8. If a domain exists, obtain/test Certbot HTTPS; otherwise document HTTP/private-classroom limitation.
9. Reboot only after recording a working rollback path and prove the service returns after reboot.
10. Practise update/rollback: record commit, update in a branch, test, restart, health-check; return to recorded commit if it fails.

---

# Lesson 12 — Present, evaluate and extend
**Effort:** medium. **Suggested Git checkpoint:** `document final evaluation`.

## Final demonstration checklist
Demonstrate: (1) dashboard, (2) OWASP content, (3) live/recent cached CVEs, (4) search/filter, (5) failure handling, (6) request architecture, (7) Git history, (8) tests, (9) security controls, (10) one design decision, (11) one diagnosed problem, (12) next feature.

### Likely questions and strong answers
* **Why cache?** “It makes pages faster and reduces NVD rate-limit pressure. If NVD fails, we label older data as stale rather than pretending it is fresh.”
* **Why Nginx and Gunicorn?** “Nginx is the public reverse proxy. Gunicorn runs Flask privately on localhost. This avoids exposing the development server.”
* **How did you handle untrusted descriptions?** “Jinja escapes template values and our JavaScript uses `textContent`, not `innerHTML`.”
* **What would you add?** Name an extension, its risk and its acceptance test.

## Optional extension cards (easy to harder)
For every extension, write: **new concept, prerequisite, approach, risk, acceptance criteria**.
1. Dark mode — localStorage; contrast; survives reload.
2. Pagination — arrays; accurate page controls; handles empty page.
3. Clickable severity bars — events; matching filter changes.
4. Chart.js — third-party library/CSP; chart has text alternative.
5. Scheduled refresh — systemd timer; no repeated rate-limit requests.
6. NVD keyword/product search — query validation; bounded results.
7. Published vs modified — date handling; labels clear.
8. CISA KEV enrichment — optional HTTP client; outage still shows CVEs.
9. CSV export — escaping; download matches filters.
10. SQLite watchlist — database basics; no secrets/unsafe queries.
11. Server-side filters — validated query parameters; automated tests.
12. Another JSON endpoint — API design; documented status/errors.
13. Private classroom authentication — credentials; HTTPS required.
14. CI workflow — GitHub Actions; tests run on push.
15. Containerisation — only after non-container deployment; explain new complexity.
16. Monitoring — uptime endpoint; useful alert, not alert noise.
17. Structured JSON logs — observability; no keys/personal data.
18. SBOM — dependency inventory; explain limits.
19. Dependency scanning — advisory triage; documented update choice.
20. Accessibility audit — WCAG evidence; keyboard, contrast and semantic fixes.

---

# Appendix A — Challenge cards

1. **No CVSS score:** a card has no score. *Hints:* inspect `None`; use the existing fallback. *Success:* “Not scored” and no crash. *Practises:* optional data.
2. **HTTP 429:** NVD limits you. *Hints:* status, TTL, cache. *Success:* friendly warning/no retry loop. *Practises:* rate limits.
3. **Timeout:** network stalls. *Hints:* timeout and mock. *Success:* cache fallback. *Practises:* resilience.
4. **Special characters:** description has markup characters. *Hints:* text node/Jinja. *Success:* text appears literally. *Practises:* XSS prevention.
5. **Stale cache:** data is older than TTL. *Hints:* timestamp/environment. *Success:* visible stale message. *Practises:* cache states.
6. **Extra port:** UFW has unnecessary rule. *Hints:* numbered rules. *Success:* exact rule removed and SSH retained. *Practises:* firewall safety.
7. **Manual works, systemd fails:** *Hints:* journal, user/path. *Success:* service starts after a documented correction. *Practises:* service context.
8. **Mobile break:** navigation overlaps. *Hints:* responsive DevTools/media query. *Success:* menu/controls usable at 320px. *Practises:* responsive CSS.
9. **No matches:** filter combination returns zero. *Hints:* result message/clear. *Success:* user understands how to recover. *Practises:* UX.
10. **New OWASP edition:** *Hints:* maintenance process. *Success:* reviewed local JSON update, validation and commit. *Practises:* content maintenance.
11. **Dependency advisory:** *Hints:* pinned version/test branch. *Success:* evidenced update or documented risk decision. *Practises:* supply chain.
12. **Explain priority:** manager asks CVSS vs KEV. *Hints:* severity/exploitation/context. *Success:* accurate 30-second answer. *Practises:* communication.

# Appendix B — Responsible AI assistance log

AI may explain errors, unfamiliar syntax, test ideas, a small function, fixtures, options and documentation. It must not write the assessed project without your understanding; receive secrets; authorise unexplained commands; replace testing; or be treated as certain security advice. Follow your provider/course disclosure rules.

|Date|Question asked|Tool|Useful response|What I verified|What I changed|What I learned|
|---|---|---|---|---|---|---|
| | | | | | | |

---

# Appendix C — Foundation labs: learn the tools before you need them

These short labs are deliberately separate from the main application. They give you a safe place to practise. Complete them in your home folder, not in `/etc`, `/usr` or the project folder. Every lab starts with a concept, then an example, then a small task. If something goes wrong, use `pwd` and `ls -la` before doing anything else.

## Lab C1 — Paths, folders and files

### Overview
A computer stores files inside folders (also called directories). A **path** is the route to a file. An **absolute path** starts at `/`, the top of the Linux filesystem: `/home/student/notes.txt`. A **relative path** starts from where you are now: `notes.txt`. `~` is a shortcut for your home folder. The shell is a program which reads commands one line at a time.

### Try it
```bash
pwd
mkdir -p ~/dashboard-lab/week1
cd ~/dashboard-lab/week1
pwd
ls -la
touch first-note.txt
ls -la
```

`touch` creates an empty file if it does not exist. It is also used to update a file timestamp. `mkdir -p` makes all missing folders in a path and does not complain if they already exist. In the output of `ls -la`, the first character `d` means directory and `-` means ordinary file.

### Guided challenge
1. Create `~/dashboard-lab/week1/assets`.
2. Enter it using `cd` and prove your location with `pwd`.
3. Create `colours.txt` with `touch`.
4. Go back one folder with `cd ..`.
5. List the contents of `assets` without entering it: `ls -la assets`.
6. Return home with `cd` on its own. Why does this work?

**Checkpoint:** you can explain absolute, relative and home-folder paths.
**Try a mistake safely:** type `cd missing-folder`. Read the error; then run `ls` to see why it failed. Do not create a random folder just to silence an error.

## Lab C2 — Read and edit text safely

### Overview
Configuration and code are text files. A command-line editor does not protect you from mistakes, so make one change, save, inspect, then continue. `nano` is included because its shortcuts appear at the bottom of the screen.

### Try it
```bash
cd ~/dashboard-lab/week1
nano first-note.txt
```
Type three short lines. Save with `Ctrl+O`, press Enter to confirm the name, then exit with `Ctrl+X`. Now run:

```bash
cat first-note.txt
less first-note.txt
```

`cat` prints a short file at once. `less` is better for long files: press Space to move down, `b` up, `/word` to search, and `q` to quit. Never use `cat` on a secret file in a shared screen recording.

### Guided challenge
1. Add a fourth line with `nano`.
2. Search the file with `grep -n 'word-you-used' first-note.txt`. `-n` adds line numbers.
3. Copy it: `cp first-note.txt backup-note.txt`.
4. Compare names with `ls -l`.
5. Rename the backup: `mv backup-note.txt checked-note.txt`.
6. Print only the final two lines: `tail -n 2 first-note.txt`.

**Checkpoint:** explain the difference between copying and moving.
**Common error:** saving a file in the wrong folder. Use `pwd` before `nano`, or use an absolute path.

## Lab C3 — Permissions in plain English

### Overview
Linux permissions decide who may read (`r`), write (`w`) or enter/execute (`x`) a file. `ls -l` shows three groups: owner, group, everyone else. A private key should not be readable by everyone. Do not solve every problem with `sudo` or `chmod 777`; that hides the question “who should really have access?”

```bash
cd ~/dashboard-lab/week1
ls -l first-note.txt
chmod 600 first-note.txt
ls -l first-note.txt
```
`600` means owner can read/write; group and others have no permissions. This is appropriate for a private text note, not necessarily a shared web asset. Restore a normal readable example with `chmod 644 first-note.txt` (owner read/write; others read).

**Checkpoint:** explain why a service account needs read permission to application files but should not own system configuration.
**Safety rule:** only change permissions on files you own in this lab. Record the old mode before changing a production file.

## Lab C4 — Processes, ports and stopping programs

### Overview
A **process** is a running program. A **port** is a numbered doorway used for network traffic. A browser normally uses 80 (HTTP) or 443 (HTTPS); the local Flask example uses 5000. A process bound to `127.0.0.1` accepts connections only from the same server.

In one terminal, run `python app.py`. In a second terminal:

```bash
ss -tulpn | grep 5000
curl -i http://127.0.0.1:5000/health
ps aux | grep '[p]ython app.py'
```

The square brackets in the last command stop `grep` finding itself. Return to the first terminal and press `Ctrl+C`; this sends an interrupt to the program you started. Run the port command again. It should no longer show port 5000.

**Checkpoint:** explain why Gunicorn later binds to `127.0.0.1:8000` and Nginx, rather than Gunicorn, is public.

## Lab C5 — Reading command help

### Overview
Good developers do not memorise every option. They find help, read the relevant part and test a small example. On Ubuntu, `man` opens a manual page, `--help` gives short help, and `apropos` searches manual titles.

```bash
mkdir --help | less
man ls
apropos 'copy files'
```
Quit a manual with `q`. Look up `cp` and identify what recursive copying means before using `cp -r`. Do not run options merely because an example contains them.

---

# Appendix D — Design studio: choose a name, type and colour system

## Overview
The reference implementation deliberately starts as **My Security Dashboard**. It is not your final product name. Naming and visual design should communicate purpose, not disguise security information. Choose your identity after the basic pages work so styling does not distract from learning the structure.

## Step 1: create a small brand brief
Pick one audience: a small IT team, an operations manager, a school technical team, or an informed learner. Pick three adjectives, such as “clear, calm, evidence-led”. Write only these three short answers in your decision record:

* Who will use the dashboard?
* What should they understand within ten seconds?
* What should they do next?

## Step 2: find a suitable font
A dashboard should use one easy-to-read body font and, at most, one heading font. Good sources are: your operating system's system font stack (fastest and no download), [Google Fonts](https://fonts.google.com/) (look at the licence and load only needed weights), [Fontshare](https://www.fontshare.com/) (check its licence), or a permitted organisation brand font. Search for a sans-serif family with regular and bold weights. Examples to compare: Inter, Atkinson Hyperlegible, Source Sans 3, Noto Sans and IBM Plex Sans.

Test the same sentence at 16px body size and 28–36px heading size. Reject a choice if the lowercase `l`, uppercase `I` and number `1` are hard to tell apart. Keep the core system font unless you can explain performance, licensing and accessibility implications of a web font.

## Step 3: choose colours with a job
Use three roles rather than random colours: dark neutral for text, light neutral for background/surfaces, and an accent for links/actions. Severity colours are extra indicators, never the only indicator. Sources for starting palettes include [Adobe Color](https://color.adobe.com/), [Coolors](https://coolors.co/), and the accessible examples in the [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/). These tools suggest colours; you still test the final text/background pairing.

1. Choose background, text and accent candidates.
2. Test normal text contrast against its exact background; aim for WCAG AA (generally 4.5:1 for ordinary text).
3. Open the existing page and use DevTools to inspect the CSS custom properties at the top of `styles.css`.
4. Change only `--blue` in a branch, refresh, test links/focus/bars, then decide whether to keep it.

## Step 4: apply your name safely
In `templates/base.html`, find the page title and brand link. In `templates/index.html`, find the `<h1>`. Change the displayed text in both places to your chosen name. Do not rename Python modules, service users, folders or deployment files merely for branding: a public label and an operating-system identifier are different things.

**Checkpoint:** keyboard users can still see which link/control has focus; page text remains readable; the name explains the dashboard purpose.
**Reflection:** why might a decorative font be unsuitable for CVE identifiers?

---

# Appendix E — Worked web-page reading exercise

## Overview
HTML gives information structure. CSS gives presentation. JavaScript responds to actions. Reading a small page from the outside in is a useful way to understand it.

### HTML example
```html
<label for="search">Search CVEs</label>
<input id="search" type="search" aria-describedby="search-help">
<p id="search-help">Search an identifier or description.</p>
```
`label` names the control; `for` connects it to the input `id`; `type="search"` tells the browser the purpose; `aria-describedby` connects helpful text. The student task is to identify a comparable label in `templates/cves.html`, then test it with keyboard focus.

### CSS example
```css
.card {
  background: var(--card);
  padding: 1rem;
  border-radius: .5rem;
}
```
A **selector** (`.card`) chooses elements with that class. A **declaration** has a property and value. `var(--card)` reuses a named colour. `1rem` is relative to base text size. Experiment in DevTools first: change `padding` from `1rem` to `2rem`; observe the result; then refresh to discard the experiment.

### JavaScript example
```javascript
const button = document.querySelector('#menu');
button.addEventListener('click', () => {
  button.setAttribute('aria-expanded', 'true');
});
```
`const` creates a named value; `querySelector` finds an element; `addEventListener` waits for a click; the arrow function runs after the click. The real code toggles rather than permanently sets the state. Find it in `dashboard.js` and test the Menu using keyboard.

---

# Appendix F — Complete worked examples and practice data

This appendix supplies the missing “see one first” stage for the main lessons. Everything labelled **invented** is made-up data for learning. Do not search for, report, scan for, or attempt to exploit these example identifiers/products. The aim is to practise reading, transforming and presenting information safely.

## F1. From a browser request to a page: one complete example

### Overview
When you type an address into a browser, the browser requests a resource. The server responds with a status, headers and a body. The page you see is not “inside” Flask: Flask sends HTML to the browser, then the browser reads CSS and JavaScript as separate requests.

### Example request and response

```text
Browser request
GET /health HTTP/1.1
Host: 127.0.0.1:5000

Server response
HTTP/1.1 200 OK
Content-Type: application/json
X-Content-Type-Options: nosniff

{"status":"ok"}
```

`GET` asks to read a resource. `/health` is the route. `200 OK` means the server completed the request successfully. `Content-Type: application/json` says the body is JSON. The body is a tiny object with one key, `status`.

### Practise
Start the app, then run these commands one at a time:

```bash
curl -i http://127.0.0.1:5000/health
curl -i http://127.0.0.1:5000/not-a-page
curl -I http://127.0.0.1:5000/
```

The first should be 200. The second should be 404, which means the route does not exist. The third uses `-I` to request headers only. Find `Content-Security-Policy`, `Referrer-Policy` and `X-Content-Type-Options`. A header is not a substitute for safe code, but it adds a browser-side layer of protection.

**Checkpoint:** write only the three status numbers you observed and what each means.
**If it fails:** first check that the app terminal is still running; then check the exact address and port; then use `ss -tulpn | grep 5000`.

## F2. Read JSON slowly: object, list and nested value

### Overview
JSON uses braces `{}` for an object: named values such as `"id": "CVE-..."`. It uses square brackets `[]` for an ordered list. Indentation makes nesting easier to see but does not change the data. A comma separates items. JSON uses `true`, `false` and `null`, not Python's `True`, `False` and `None`.

### Invented small response

```json
{
  "totalResults": 2,
  "vulnerabilities": [
    {
      "cve": {
        "id": "CVE-2026-90001",
        "published": "2026-03-01T09:30:00.000",
        "descriptions": [
          {"lang": "en", "value": "Invented archive service example."},
          {"lang": "fr", "value": "Exemple inventé."}
        ],
        "metrics": {
          "cvssMetricV31": [
            {"cvssData": {"version": "3.1", "baseScore": 9.8, "baseSeverity": "CRITICAL"}}
          ]
        }
      }
    },
    {
      "cve": {
        "id": "CVE-2026-90002",
        "descriptions": [],
        "metrics": {}
      }
    }
  ]
}
```

Follow the first score with this route: root object → `vulnerabilities` list → first item `[0]` → `cve` object → `metrics` object → `cvssMetricV31` list → first item `[0]` → `cvssData` object → `baseScore`. This explains why API code can look long even when the final displayed value is only `9.8`.

### Practise with Python
Create a scratch file named `read_json.py` in `~/dashboard-lab`:

```python
import json
from pathlib import Path

text = Path("tests/fixtures/nvd_sample.json").read_text()
payload = json.loads(text)
first = payload["vulnerabilities"][0]["cve"]
print(first["id"])
print(first["descriptions"][0]["value"])
print(first["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"])
```

This is a **provided learning example**. `import` makes a module available; `Path` represents a file path; `.read_text()` reads text; `json.loads()` changes JSON text into Python dictionaries/lists; square brackets select a known key or list position. Run `python read_json.py` from a folder where the relative fixture path is correct, or replace it with an absolute path.

**Experiment 1:** change `[0]` to `[1]` for the second record and observe the error when it has no description. Restore it.
**Experiment 2:** print `payload["totalResults"]`. Explain why this is easier: it is directly inside the root object.
**Likely error:** `KeyError` means a dictionary key is missing; `IndexError` means a requested list position is absent. Robust application code uses `.get` and fallback values where external data may be incomplete.

## F3. Normalisation worked example: complex input to small model

### Overview
Normalisation creates a dependable internal shape. It is like moving ingredients from differently shaped packets into labelled containers before cooking. Templates then use one predictable list of fields instead of needing to understand NVD's full format.

### Input and output comparison

|Upstream concept|Possible NVD location|Internal dashboard value|
|---|---|---|
|Identifier|`cve.id`|`id`|
|English description|one item in `cve.descriptions`|`description`|
|Base score|one CVSS metric version|`score`|
|Severity|same metric|`severity`|
|Weakness names|nested `weaknesses` descriptions|`weaknesses` list|
|External link|built from identifier|`nvd_url`|

For the invented first record, the normalised result looks like:

```python
{
    "id": "CVE-2026-90001",
    "description": "Invented archive service example.",
    "published": "2026-03-01T09:30:00.000",
    "last_modified": None,
    "score": 9.8,
    "severity": "CRITICAL",
    "cvss_version": "3.1",
    "weaknesses": [],
    "nvd_url": "https://nvd.nist.gov/vuln/detail/CVE-2026-90001",
    "known_exploited": False,
    "kev_details": None,
}
```

Notice `None`: Python uses it for an absent value. The template displays “Not supplied” or “Not scored” rather than inventing a value. An absent score is not zero.

### Practise without editing the app

```bash
python - <<'PY'
import json
from pathlib import Path
from services.normalisers import normalise_response

source = json.loads(Path('tests/fixtures/nvd_sample.json').read_text())
for cve in normalise_response(source):
    print(cve['id'], '|', cve['severity'], '|', cve['score'])
PY
```

Read the output. Then open `services/normalisers.py` alongside `tests/fixtures/nvd_sample.json`. Highlight each place the normaliser protects against missing values. Do not change it yet.

**Checkpoint:** explain why a page template should receive the small model rather than the whole NVD response.

## F4. Cache timeline worked example

### Overview
A cache has a timestamp. The **time to live** (TTL) is the maximum age considered fresh. The app must distinguish fresh cached data, live data and stale fallback data so users are not misled.

Assume `CACHE_TTL_SECONDS=1800` (30 minutes):

|Time|What happens|What the user should see|
|---|---|---|
|09:00|NVD succeeds; 20 normalised records are written|“Last refreshed 09:00”; normal dashboard|
|09:10|Page reloads; cache is 10 minutes old|Same data quickly; no NVD request needed|
|09:31|Cache is 31 minutes old; NVD succeeds|New cache written; normal dashboard|
|10:02|Cache is 31 minutes old; NVD times out|Older records plus clear “Showing older cached data” warning|
|10:05|No cache exists; NVD fails|Friendly unavailable-data message, not traceback|

The cache file contains data and `fetched_at`; it must never contain the API key. Atomic replacement means the application writes a temporary completed JSON file and replaces the old one only when ready.

### Practise
Run the test that demonstrates stale fallback:

```bash
pytest -q tests/test_cache.py -vv
```

`-vv` gives more test names/detail. Read the test before and after running it. Find the mock that deliberately makes NVD fail. This is safer than turning off a real network connection.

**Reflection:** Why is “always show the last result with no warning” misleading?
**Answer:** users could make a time-sensitive decision believing old data is current.

## F5. Safe text rendering worked example

### Overview
An API description is data from outside the application. It may contain characters with special meaning in HTML. Treat it as text. The dashboard's JavaScript creates a paragraph and sets `.textContent`; it does not feed untrusted data into `.innerHTML`.

### Invented description

```text
Invented example: text containing <strong>words</strong> and & symbols.
```

When displayed safely with `textContent`, the browser shows the angle brackets as characters. It does **not** make the word bold. This is desirable because the application should decide its own HTML structure.

### Safe and unsafe comparison

```javascript
// Safe: the browser treats the value as text.
paragraph.textContent = description;

// Do not use this with external API data: it asks the browser to parse HTML.
paragraph.innerHTML = description;
```

Do not test dangerous browser payloads. The harmless invented string above is enough to observe the difference. In Jinja templates, `{{ cve.description }}` is escaped by default. Do not add `|safe` to external content.

### Practise
Use browser DevTools Console on a local page:

```javascript
const example = document.createElement('p');
example.textContent = 'Words with <strong>angle brackets</strong>.';
document.body.append(example);
```

Observe the page. Remove the temporary element by refreshing. This is a local visual experiment, not a code change.

## F6. Filter logic worked example

### Overview
A filter asks whether each record meets conditions. All selected conditions must match. Sorting changes order; it does not remove records. The dashboard filters in the browser after receiving normalised data.

Use this invented list:

|ID|Severity|Score|Known exploited|Published|
|---|---:|---:|---|---|
|CVE-2026-90001|CRITICAL|9.8|No|2026-03-01|
|CVE-2026-90002|HIGH|8.1|Yes|2026-03-02|
|CVE-2026-90003|MEDIUM|5.4|No|2026-03-03|
|CVE-2026-90004|HIGH|not scored|No|2026-03-04|

Try these predictions before using the UI:

1. Severity HIGH → records `90002` and `90004`.
2. Minimum score 8.0 → `90001` and `90002`; the not-scored record is not included.
3. Known exploited only → `90002`.
4. HIGH plus known exploited → only `90002`.
5. HIGH plus minimum score 9.0 → no matches; the empty-state message should explain what happened.

Open `/cves` and repeat with real cached fixture data. Use Clear filters between attempts. If a result surprises you, read the values shown on each card before assuming the code is wrong.

## F7. Testing worked example: Arrange, Act, Assert

### Overview
A test says what the program should do in a particular situation. It is a safety net, not proof that every possible problem is absent. Use small, repeatable test data.

```python
def test_unscored_record_has_safe_fallback():
    # Arrange: make a tiny upstream record without metrics.
    upstream = {"cve": {"id": "CVE-2026-90004", "descriptions": [], "metrics": {}}}

    # Act: convert it using the normaliser.
    result = normalise_cve(upstream)

    # Assert: check the two important promises.
    assert result["score"] is None
    assert result["description"] == "No English description supplied."
```

This example uses invented data. `def` starts a function. Comments explain test stages. `assert` fails the test when its condition is false. The existing test suite follows the same idea using fixtures.

### Practise
1. Read `tests/test_normalisers.py`.
2. Identify its Arrange, Act and Assert statements with comments in your notebook or evidence record.
3. Run one file: `pytest -q tests/test_normalisers.py`.
4. Change one expected value in a temporary local copy, run the test, read the failure, then undo the change with `git restore tests/test_normalisers.py`.

This is a controlled failure. It teaches that a red test contains useful information: expected value, actual value and line number.

## F8. Git worked example: a small, recoverable change

### Overview
Commit after one understandable improvement. A commit message explains intent, not every keystroke. Git lets you inspect before recording and recover after a mistake.

```bash
git status
git diff
git add templates/index.html
git commit -m "Add dashboard audience statement"
git log --oneline -3
```

Imagine `git diff` shows only your one sentence. `git add templates/index.html` stages just that file; `git commit` makes a snapshot; `git log --oneline -3` shows recent snapshots. If `git status` unexpectedly lists `.env`, stop: it must not be staged.

### Practise recovery
Make a harmless visible text change, commit it, then decide it was not wanted:

```bash
git log --oneline -1
git revert HEAD
git log --oneline -2
```

`git revert` creates a new commit that reverses the previous commit. It is safer for shared history than changing old commits. Open the page to confirm the text returned to its earlier state.

## F9. Deployment diagnosis worked example

### Scenario
You run `systemctl status vulnerability-dashboard --no-pager` and see `Active: failed`. The public Nginx page displays `502 Bad Gateway`.

### Reasoning route
1. A 502 means Nginx could not get a suitable response from the upstream application. It does not automatically mean Nginx is broken.
2. On the server, run `curl -i http://127.0.0.1:8000/health`. If it cannot connect, investigate Gunicorn/systemd first.
3. Run `journalctl -u vulnerability-dashboard -n 50 --no-pager`. Read the first relevant error line.
4. Suppose it says the Python executable does not exist. Compare `ExecStart` in `/etc/systemd/system/vulnerability-dashboard.service` with `ls -l /srv/vulnerability-dashboard/.venv/bin/gunicorn`.
5. Correct only the path, run `sudo systemctl daemon-reload`, then `sudo systemctl restart vulnerability-dashboard`.
6. Re-test local health, then `sudo nginx -t`, then public page. Record the evidence.

Do not restart every service repeatedly without reading logs. The order above identifies which layer failed and proves the repair.
