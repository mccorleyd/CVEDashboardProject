# Independent Ubuntu deployment lesson

This guide is deliberately written as a sequence of small, checkable steps. Read every explanation before typing its command. Keep one SSH session open while changing SSH or firewall rules. Open a second session to prove access still works. If you do not control the cloud account, complete the local parts and record the commands you would run rather than guessing.

## 1. What production deployment changes

Your local Flask server is for learning: it restarts when the terminal closes and is not designed to face the public internet. Production uses three layers:

```text
Internet browser → Nginx on ports 80/443 → Gunicorn on 127.0.0.1:8000 → Flask
```

Nginx is the public front door. Gunicorn runs Python. systemd starts Gunicorn after reboot and records logs. The service user has only the access required for the project. The cache stays on the server. Do not open port 8000 in UFW or your cloud-provider firewall.

## 2. Record your values once

In your private setup notes, write the following values. Do not put passwords or keys in Git.

|Meaning|Example only|
|---|---|
|Server public address|`203.0.113.10`|
|SSH user|`ubuntu`|
|Repository URL|private Git URL|
|Application folder|`/srv/vulnerability-dashboard`|
|Service user|`vulnerability-dashboard`|
|Domain, if owned|`dashboard.example.org`|

The example IP/domain are reserved examples. Replace them only in commands that explicitly need your own value.

## 3. Connect and inspect

```bash
ssh -i YOUR_KEY_FILE ubuntu@YOUR_SERVER_ADDRESS
whoami
hostname
pwd
sudo ss -tulpn
```

`hostname` identifies the server; `ss` shows listening services. Save the output. You should be able to explain why an unknown listening service needs investigation before deployment.

## 4. Update safely and create a service account

```bash
sudo apt update
sudo apt upgrade
sudo adduser --system --group --home /srv/vulnerability-dashboard vulnerability-dashboard
id vulnerability-dashboard
```

`apt update` refreshes the package list; `apt upgrade` installs available updates. The account is a system account intended to run the application, not an administrator login. Verify it exists using `id`. If you made this account by mistake before installing files, remove it with `sudo deluser --remove-home vulnerability-dashboard`.

Before editing SSH configuration, take a provider snapshot if available. Check syntax before reload:

```bash
sudo sshd -t
```

Only after key-based login succeeds in a **second** terminal should you consider disabling password authentication. Do not use root login for this project.

## 5. Install packages and copy the project

```bash
sudo apt install -y git python3-venv python3-pip nginx curl
sudo mkdir -p /srv/vulnerability-dashboard /etc/vulnerability-dashboard
sudo chown vulnerability-dashboard:www-data /srv/vulnerability-dashboard
sudo -u vulnerability-dashboard git clone YOUR_REPOSITORY_URL /srv/vulnerability-dashboard
sudo -u vulnerability-dashboard python3 -m venv /srv/vulnerability-dashboard/.venv
sudo -u vulnerability-dashboard /srv/vulnerability-dashboard/.venv/bin/pip install -r /srv/vulnerability-dashboard/requirements.txt
```

Check each command before moving on. `sudo -u vulnerability-dashboard` runs only that command as the low-privilege account. Verify ownership with:

```bash
ls -ld /srv/vulnerability-dashboard
sudo -u vulnerability-dashboard /srv/vulnerability-dashboard/.venv/bin/python --version
```

If `git clone` fails, read the message. A private repository may need a deploy key or an HTTPS credential method supplied by the repository host; do not paste personal passwords into shell history.

## 6. Create the secret environment file

The systemd service reads configuration from a root-owned file, not from `.env` in Git.

```bash
sudo install -o root -g vulnerability-dashboard -m 0640 /dev/null /etc/vulnerability-dashboard/vulnerability-dashboard.env
sudo nano /etc/vulnerability-dashboard/vulnerability-dashboard.env
```

Enter these lines, replacing only the secret value with a long random value. Leave `NVD_API_KEY` empty if you do not have one.

```text
SECRET_KEY=replace_this_with_a_long_unique_random_value
NVD_API_KEY=
CACHE_TTL_SECONDS=1800
CVE_RESULTS_PER_PAGE=20
ENABLE_CISA_KEV=true
```

Save, then verify that the service account can read but not write it:

```bash
sudo -u vulnerability-dashboard test -r /etc/vulnerability-dashboard/vulnerability-dashboard.env && echo readable
ls -l /etc/vulnerability-dashboard/vulnerability-dashboard.env
```

Do not display this file on a shared screen. If it is accidentally committed, rotate the secret and remove it from Git history following your repository provider's incident guidance.

## 7. Test Gunicorn before systemd

```bash
cd /srv/vulnerability-dashboard
sudo -u vulnerability-dashboard .venv/bin/gunicorn --workers 2 --bind 127.0.0.1:8000 'app:create_app()'
```

Keep this terminal running. In a second SSH terminal:

```bash
curl -i http://127.0.0.1:8000/health
curl -I http://127.0.0.1:8000/
```

Expect `200` and JSON from `/health`. `127.0.0.1` proves the app is private to the server. Stop manual Gunicorn with `Ctrl+C`. If it fails, do not start Nginx yet: check active virtual environment paths, working directory, `requirements.txt`, and the error printed by Gunicorn.

## 8. Install the systemd service

```bash
sudo cp /srv/vulnerability-dashboard/deployment/vulnerability-dashboard.service /etc/systemd/system/vulnerability-dashboard.service
sudo systemctl daemon-reload
sudo systemctl enable --now vulnerability-dashboard
sudo systemctl status vulnerability-dashboard --no-pager
```

`daemon-reload` tells systemd that a unit file changed. `enable` starts at boot; `--now` starts it now. Verify again:

```bash
curl -i http://127.0.0.1:8000/health
journalctl -u vulnerability-dashboard -n 50 --no-pager
```

If it fails, use the journal output before changing files. Typical causes are a wrong absolute path in `ExecStart`, unreadable environment file, a missing dependency, or incorrect ownership. After changing the unit file, run `daemon-reload` again, then `sudo systemctl restart vulnerability-dashboard`.

## 9. Configure Nginx

The provided Nginx configuration is intentionally small. Copy it, then edit `server_name`.

```bash
sudo cp /srv/vulnerability-dashboard/deployment/nginx-vulnerability-dashboard.conf /etc/nginx/sites-available/vulnerability-dashboard
sudo nano /etc/nginx/sites-available/vulnerability-dashboard
sudo ln -s /etc/nginx/sites-available/vulnerability-dashboard /etc/nginx/sites-enabled/vulnerability-dashboard
sudo nginx -t
sudo systemctl reload nginx
```

Set `server_name` to your real domain if you have one. For a temporary private-IP test, use `_`; never claim a trusted public certificate is configured for a private IP. `nginx -t` is a syntax test; if it fails, do **not** reload. Check the site:

```bash
curl -I http://127.0.0.1/
sudo tail -n 30 /var/log/nginx/access.log
sudo tail -n 30 /var/log/nginx/error.log
```

The configuration uses a request-rate zone. This is a simple protection against bursts, not a complete denial-of-service solution.

## 10. Configure UFW and cloud firewall

First keep SSH reachable. In your existing session:

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw status numbered
sudo ufw enable
sudo ufw status verbose
```

Then open a **second** SSH connection and load the site. If locked out, use the cloud console/recovery path. Remove an accidental rule by its displayed number: `sudo ufw delete NUMBER`. Your cloud-provider firewall must also allow only required traffic: SSH from trusted addresses where possible, HTTP/HTTPS as needed. Verify that Gunicorn port 8000 is not public with `sudo ss -tulpn` and provider rules.

## 11. DNS and HTTPS

If you own a domain, create an A (and where appropriate AAAA) DNS record pointing to the public server address. Wait until this returns your address:

```bash
dig +short YOUR_DOMAIN
```

Then install Certbot using the current official instructions for Ubuntu and run the Nginx certificate command for your domain, for example `sudo certbot --nginx -d YOUR_DOMAIN`. Test `https://YOUR_DOMAIN`, then test renewal using Certbot's documented dry-run. A trusted public certificate normally cannot be issued for a bare private IP address; document that limitation rather than bypassing browser warnings.

## 12. Verify, update and roll back

### Verification checklist
```bash
systemctl is-active vulnerability-dashboard
curl -i http://127.0.0.1:8000/health
sudo nginx -t
journalctl -u vulnerability-dashboard -n 30 --no-pager
```

Also test public home page, CSS, CVE explorer, stale warning, headers (`curl -I URL`), keyboard navigation and a reboot only after recording a known-good Git commit.

### Safe update
```bash
cd /srv/vulnerability-dashboard
sudo -u vulnerability-dashboard git status
sudo -u vulnerability-dashboard git fetch --tags
sudo -u vulnerability-dashboard git checkout TAG_OR_COMMIT
sudo -u vulnerability-dashboard .venv/bin/pip install -r requirements.txt
sudo -u vulnerability-dashboard .venv/bin/pytest -q
sudo systemctl restart vulnerability-dashboard
curl -i http://127.0.0.1:8000/health
```

Record the previous commit before checking out a new one. If health/tests fail, return to the recorded commit, install its requirements, restart and test again. Back up the Nginx site, unit file and non-secret configuration records. Do not back up live keys into a public location.

### Removal
Disable the service, remove its Nginx symlink/site, test/reload Nginx, delete UFW rules only when no longer needed, and preserve required evidence/logs. Remove service user and project directory only after confirming no other service uses them.
