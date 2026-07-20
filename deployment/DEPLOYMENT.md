# Ubuntu deployment guide
## Prerequisites and safe hardening
Use Ubuntu 24.04 LTS/current supported LTS, provider firewall and SSH key. Keep the first SSH session open; open a **second** connection before disabling password authentication. `sudo apt update && sudo apt upgrade` changes packages; verify `apt` completes; rollback is package-specific/snapshot. Create least-privilege user: `sudo adduser --system --group --home /srv/cyberscope cyberscope` (verify `id cyberscope`; undo `sudo deluser --remove-home cyberscope`). Review `/etc/ssh/sshd_config` and test `sudo sshd -t`; only after second key login succeeds set password authentication off and `sudo systemctl reload ssh`. Firewall: `sudo ufw allow OpenSSH`, verify `sudo ufw status`, then `sudo ufw enable`; undo `sudo ufw disable` or delete a named rule. Later `sudo ufw allow 'Nginx Full'`; only SSH/HTTP(S) should listen (`ss -tulpn`).

## Install and run
```bash
sudo apt install -y git python3-venv nginx
sudo mkdir -p /srv/cyberscope-dashboard /etc/cyberscope
sudo chown cyberscope:www-data /srv/cyberscope-dashboard
sudo -u cyberscope git clone YOUR_REPOSITORY /srv/cyberscope-dashboard
sudo -u cyberscope python3 -m venv /srv/cyberscope-dashboard/.venv
sudo -u cyberscope /srv/cyberscope-dashboard/.venv/bin/pip install -r /srv/cyberscope-dashboard/requirements.txt
sudo install -o root -g cyberscope -m 0640 /dev/null /etc/cyberscope/cyberscope.env
sudo nano /etc/cyberscope/cyberscope.env
```
Put `SECRET_KEY=...`, optional `NVD_API_KEY=...`, `CACHE_TTL_SECONDS=1800`; verify `sudo -u cyberscope test -r /etc/cyberscope/cyberscope.env`. Never put secrets in Git. Test from project: `sudo -u cyberscope .venv/bin/gunicorn --bind 127.0.0.1:8000 'app:create_app()'`; in a second terminal `curl -i http://127.0.0.1:8000/health`, then stop it.

## systemd and Nginx
Copy `deployment/cyberscope.service` to `/etc/systemd/system/`, then `sudo systemctl daemon-reload && sudo systemctl enable --now cyberscope && sudo systemctl status cyberscope`. Copy `nginx-cyberscope.conf` to `/etc/nginx/sites-available/cyberscope`, set real `server_name`, symlink into `sites-enabled`, remove default if appropriate, run `sudo nginx -t`, then `sudo systemctl reload nginx`. Verify public `/health`, `/`, static CSS and `journalctl -u cyberscope -n 50`. Browser → Nginx → Gunicorn → Flask → API/cache.

## DNS, HTTPS, update/rollback/cleanup
Point A/AAAA record to public IP, wait for `dig +short DOMAIN`, then `sudo snap install certbot --classic` or distro Certbot and `sudo certbot --nginx -d DOMAIN`; test renewal. A trusted public certificate normally cannot be issued for a bare private IP. Update: `git fetch`, record current commit/tag, `git checkout TAG_OR_COMMIT`, install requirements, `pytest`, restart, health-check. Roll back by checking out recorded commit and restart. Back up `/etc/cyberscope`, Nginx site and service config securely (not secrets in public storage). Cleanup: disable service, remove site/symlink/firewall rule/app user only after preserving needed evidence/logs.
