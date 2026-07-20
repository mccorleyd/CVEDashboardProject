# Independent Ubuntu deployment lesson

This guide is deliberately written as a sequence of small, checkable steps. Read every explanation before typing its command. **Every command below is typed into LISH** (Linode's browser-based console, opened from the Linode Cloud Manager) — not SSH, which your network blocks and which this server does not need you to use. Unlike a normal SSH-based deployment, you do not need to keep a second session open "in case you get locked out": LISH is unaffected by firewall or SSH misconfiguration, because it connects at a lower level than the network stack. If you do not control the cloud account, complete the local parts and record the commands you would run rather than guessing.

## 1. What production deployment changes

Your local Flask server is for learning: it runs on your laptop, restarts when the terminal closes, and is not designed to face the public internet. Production uses three layers on the Linode server:

```text
Internet browser → Nginx on ports 80/443 → Gunicorn on 127.0.0.1:8000 → Flask
```

Nginx is the public front door. Gunicorn runs Python. systemd starts Gunicorn after reboot and records logs. The service user has only the access required for the project. The cache stays on the server. Do not open port 8000 in UFW or the Linode Cloud Firewall.

Code reaches this server in only one way: you push commits from your laptop to your **public GitHub repository**, then pull them down here with `git pull`. There is no direct connection, file copy, or upload from your laptop to this server at any point — see the STUDENT_GUIDE.md section 0 diagram if any of this is unfamiliar.

## 2. Record your values once

In your private setup notes, write the following values. Do not put passwords in Git — but note there are no SSH keys to manage in this workflow at all.

|Meaning|Example only|
|---|---|
|Linode public IP address|`203.0.113.10`|
|GitHub repository URL (public)|`https://github.com/YOUR-USERNAME/vulnerability-dashboard.git`|
|Application folder|`/srv/vulnerability-dashboard`|
|Service user|`vulnerability-dashboard`|
|Domain, if owned|`dashboard.example.org`|

The example IP/domain are reserved examples. Replace them only in commands that explicitly need your own value.

## 3. Open LISH and inspect the server

From the Linode Cloud Manager, open your Linode and click **Launch LISH Console**. Log in with your own sudo user (created in Lesson 2 of the student guide, not `root`).

```bash
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

Ubuntu runs `sshd` by default even though you never use it yourself; reviewing its configuration is still good practice, since it is reachable from the internet regardless. Check syntax before reload:

```bash
sudo sshd -t
```

Do not use root login for this project, and do not rely on SSH password authentication — you have no legitimate reason to expose it at all, since your access route is LISH (see step 10, which closes port 22 at the network edge entirely).

## 5. Install packages and clone the project

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

**Because your repository is public, this `git clone` needs no credentials at all** — no SSH key, no deploy key, no GitHub sign-in. Anyone, including this server, can read a public repository over plain HTTPS. This is one of the practical advantages of the public-repo workflow: cloning onto the server is the simplest step in this whole guide. If `git clone` still fails, read the message carefully — a typo in the URL or a repository that is not actually public yet are the two most common causes.

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

Keep this terminal running. In a second LISH tab/window:

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

## 10. Configure UFW and the Linode Cloud Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw status numbered
sudo ufw enable
sudo ufw status verbose
```

Then load the site in a browser to confirm it still works. If something goes wrong, LISH is unaffected — you cannot be locked out this way. Remove an accidental rule by its displayed number: `sudo ufw delete NUMBER`.

Now add the second, independent layer: in the Linode Cloud Manager, open **Firewalls**, create one attached to this Linode, and allow only inbound TCP 80 and 443. **Do not allow inbound TCP 22** — you only ever reach this server through LISH, so there is no legitimate reason for port 22 to be reachable from the public internet at all, and closing it removes a whole category of attack. Verify that Gunicorn's port 8000 is not public either, with `sudo ss -tulpn` and the Cloud Firewall rules.

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

### Safe update: the day-2 workflow
Every future change follows the same short loop. It starts on your laptop, not here:

```text
1. Edit code locally in VS Code, test with pytest -q and python app.py
2. git add / git commit / git push   (to your public GitHub repository)
3. Open LISH and run the commands below
```

Then, in LISH:
```bash
cd /srv/vulnerability-dashboard
sudo -u vulnerability-dashboard git status
sudo -u vulnerability-dashboard git fetch --tags
sudo -u vulnerability-dashboard git pull
sudo -u vulnerability-dashboard .venv/bin/pip install -r requirements.txt
sudo -u vulnerability-dashboard .venv/bin/pytest -q
sudo systemctl restart vulnerability-dashboard
curl -i http://127.0.0.1:8000/health
```

`git pull` needs no credentials, for the same reason `git clone` did in step 5: the repository is public. Record the previous commit (`git log --oneline -1` before pulling) so you can return to it if health checks or tests fail after an update: `git checkout PREVIOUS_COMMIT`, reinstall requirements, restart, retest. If `git pull` reports a conflict, something on the server was hand-edited outside of Git — prefer `git checkout -- <file>` to discard the local change and keep GitHub as the single source of truth, rather than trying to merge server-side edits. To deploy a specific tagged release instead of the latest commit, use `git checkout TAG_NAME` after fetching tags. Back up the Nginx site, unit file and non-secret configuration records. Do not back up live keys into a public location.

### Removal
Disable the service, remove its Nginx symlink/site, test/reload Nginx, delete UFW rules only when no longer needed, and preserve required evidence/logs. Remove service user and project directory only after confirming no other service uses them.
