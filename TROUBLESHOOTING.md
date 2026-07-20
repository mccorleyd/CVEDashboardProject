# Troubleshooting and manual test plan
## Diagnose, do not guess
Record URL, time, command, status and exact output. DevTools Console finds JS errors; Network shows status/static files. Use `curl -i URL`, `ss -tulpn`, `ps aux | grep gunicorn`, `systemctl status cyberscope`, `journalctl -u cyberscope -n 100 --no-pager`, `tail -n 100 /var/log/nginx/error.log`, `dig example.org`, and `namei -l PATH` for permissions.

## Decision trees
**Site will not load** → DNS/IP reachable? → UFW/provider port 80? → Nginx `systemctl status` → error log. **Nginx page but no app** → `nginx -t` → Gunicorn service → curl `127.0.0.1:8000/health` → proxy path. **Gunicorn fails** → journal → virtualenv ExecStart → working directory/user/read permissions → `sudo systemctl daemon-reload`. **NVD error** → status 429/500/timeout → do not retry loop → inspect cache timestamp → friendly stale message. **Empty data** → cache/API response → date window → fixture test → missing fields. **CSS/JS missing** → Network 404 → static URL/template → Nginx proxy. **Local works, Nginx not** → Host header/proxy, port bound localhost, config test. **Stops after logout** → use systemd, not terminal process. **Permission error** → owner/group/execute directories, never run app as root.

## Manual plan
Test desktop and narrow mobile; tab/Enter controls; all filters and clear; empty state; API failure/stale cache/broken fixture; links; console clean; Nginx reload; service restart/reboot; headers with `curl -I`. Expected result, actual result, evidence, tester/date and fix commit should be recorded.
