# Vulnerability Dashboard troubleshooting workbook

## A method before a fix
Write down: time, URL/command, expected result, actual result, exact error/status, current folder (`pwd`), active Python (`which python`), and what changed last (`git diff`, `git log -1`). Make one change at a time. A traceback is useful to developers; do not show one to visitors.

**Two machines, two problem spaces.** First decide whether the problem is on your **laptop** (local dev server, tests, a file that will not save) or on the **Linode server** (the live site, a service that will not start). Server-side commands below are typed into **LISH**, opened from the Linode Cloud Manager — never SSH, which your network blocks.

## Quick diagnostic tools

|Question|Command/tool|How to read it|
|---|---|---|
|Where am I?|`pwd`|Use before relative paths|
|What files/ownership?|`ls -la`, `namei -l PATH`|Directory execute permission matters too|
|Which Python?|`which python`, `python --version`|Expect `.venv/bin/python` in development|
|Is a process listening?|`sudo ss -tulpn` (server) / `netstat -ano \| findstr :5000` (Windows laptop)|Find port/process; do not kill unknown process|
|Does Flask answer locally?|`curl -i http://127.0.0.1:8000/health`|200 plus JSON after Gunicorn|
|Does service run?|`systemctl status vulnerability-dashboard --no-pager`|Read active/exit code|
|Why did it fail?|`journalctl -u vulnerability-dashboard -n 100 --no-pager`|Read newest relevant error first|
|Does Nginx config parse?|`sudo nginx -t`|Must pass before reload|
|What did Nginx receive?|`sudo tail -n 50 /var/log/nginx/access.log`|Status/URL/client|
|What did Nginx reject?|`sudo tail -n 50 /var/log/nginx/error.log`|Proxy/static/config clues|
|Does browser load assets?|DevTools Network/Console|404/blocked JS/CSS errors|
|Does DNS point correctly?|`dig +short DOMAIN`|Should show intended public IP|
|Is the server's copy up to date?|`git log --oneline -1` on the server vs. `git log --oneline -1` on your laptop|Server should match the commit you last pushed and pulled|

## Decision trees

### “The site will not load”
1. Is the correct URL/domain used? Try `curl -I http://PUBLIC_IP` from a permitted client.
2. Does the Linode Cloud Firewall allow 80/443, and does UFW show only intended rules? `sudo ufw status numbered`.
3. Is Nginx active? `systemctl status nginx --no-pager`.
4. Is something listening on 80/443? `sudo ss -tulpn`.
5. Read Nginx error log. Do not change DNS/firewall and Nginx at the same time.

### “I can't push my commits to GitHub”
1. Read the exact error. `remote: Support for password authentication was removed` means you are being asked for a password where GitHub now expects the sign-in flow or a Personal Access Token — see Lesson 4.2 of the student guide.
2. If VS Code never showed a "Sign in with GitHub" prompt, open the Accounts icon (bottom-left) and sign in manually, then retry the push.
3. `Permission to X/Y.git denied` usually means you are signed in as the wrong GitHub account, or you are trying to push to a repository that is not yours — check `git remote -v` matches your own repository URL.
4. A rejected push saying the remote contains work you do not have locally means someone (or another device of yours) pushed since your last pull: run `git pull` first, resolve any conflict, then push again.

### “LISH is unresponsive or shows a blank screen”
1. Press Enter — Weblish sometimes needs a keypress to display the current prompt.
2. Resize the browser window; the terminal occasionally needs a nudge to redraw.
3. Close the LISH tab and relaunch it from the Linode Cloud Manager. This never affects the server itself — LISH is only a viewer onto it.
4. If login fails outright, confirm the password with the Cloud Manager's Reset Root Password option (this reboots the Linode), then log in as root and re-create your own user if it was lost.

### “Nginx loads but the application does not”
1. Run `sudo nginx -t`; only reload after success.
2. Run `curl -i http://127.0.0.1:8000/health` on the server. If this fails, diagnose Gunicorn first.
3. Check `systemctl status vulnerability-dashboard` and `journalctl -u vulnerability-dashboard -n 100`.
4. Compare Nginx `proxy_pass` port to Gunicorn `--bind`. Both must be `127.0.0.1:8000` in the provided files.
5. Check `WorkingDirectory`, service user and readable files.

### “Gunicorn works manually but systemd fails”
1. Manual shell may have an activated venv/environment; systemd does not.
2. Read `journalctl -u vulnerability-dashboard`, not just `systemctl status`.
3. Check absolute `ExecStart` path, `WorkingDirectory`, `User`, `Group`, `EnvironmentFile` and its permissions.
4. After unit edits: `sudo systemctl daemon-reload`, then restart/status.

### “NVD returns an error or data is empty”
1. Identify status: 429 means slow down/cache; 500 means upstream; timeout means waiting limit/network; invalid JSON means treat it as unavailable.
2. Check `instance/cache/cves.json` and its `fetched_at`; never expose its internal details to visitors.
3. Start with `tests/fixtures/nvd_sample.json`; run tests to prove normalisation works without internet.
4. Check date window/results configuration and application logs. Do not repeatedly call NVD.

### “CSS/JavaScript does not load”
1. DevTools Network: is it 404, 403, cached, or blocked by CSP?
2. Check template `url_for('static', filename=...)`, filename case and browser hard refresh.
3. Locally request `/static/css/styles.css`; through Nginx check proxy/static configuration.
4. Console syntax errors point to file/line. Restore a small known-good change with Git if necessary.

### “Permission denied”
1. Identify current user (`whoami`) and file owner/mode (`ls -l`).
2. Walk the path using `namei -l PATH`.
3. Decide the minimum owner/group/read/execute access needed. Never use `chmod 777` as a fix.
4. For service files, confirm `vulnerability-dashboard` can read app/cache and group can read environment file as configured.

## Manual test plan

|Area|Action|Expected evidence|
|---|---|---|
|Desktop/mobile|Use browser and 320px responsive mode|No overlap; menu works|
|Keyboard|Tab/Shift+Tab/Enter/Space every control|Visible focus and usable order|
|Search/filter|Use each filter and clear|Correct count/results|
|Empty state|Search impossible term|Helpful message|
|External failure|Use mocked/blocked refresh with cache|Stale warning; no traceback|
|Broken data|Run missing-value fixture tests|No crash/no false score|
|Links|Open internal/official links|Correct destination/new-tab safety|
|Restart|Restart service/Nginx|Health returns; logs clean|
|Console|Open DevTools Console|No new JS errors|
|Headers|`curl -I URL`|CSP/referrer/MIME/frame headers|

Record tester, date, expected, actual, screenshot/log, defect and commit that fixed it.
