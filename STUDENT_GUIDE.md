# Vulnerability Dashboard student workbook

**Audience:** Digital T Level students building and deploying a security dashboard.
**Project outcome:** a small, accessible security dashboard, developed on your own laptop and hosted on a Linode cloud server, deployed the same way real small applications are deployed.
**How long:** a guided project, best spread across several study sessions. Linux, Python, HTML/CSS/JavaScript and deployment each need real time — do not rush server-security or web-foundations lessons to save a day.

**Your working pattern for the whole project:** write and test code on your own laptop in VS Code; commit and push it to **your own public GitHub repository**; then, separately, log into your Linode server through its browser-based **LISH console** (not SSH — your network blocks it, and the server is never reachable directly from your laptop) and pull the same code down to run it for real. Section 0 below explains this in full before you touch a terminal.

> **Important safety rule:** never paste an API key, private SSH key, password or a server IP that is not public into chat, screenshots, Git, or an AI tool. Because your GitHub repository is **public**, this matters even more than usual: anything you commit is visible to anyone on the internet, forever, even if you later delete it in a new commit. Never run a command on the Linode server unless you can say what it will do and how to check it worked.

## Contents
0. [Start here: the map of the project](#0-start-here-the-map-of-the-project)
1. [Understand the problem and plan your dashboard](#lesson-1--understand-the-problem-and-plan-your-dashboard)
2. [Linux foundations: connect to your Linode server with LISH](#lesson-2--linux-foundations-connect-to-your-linode-server-with-lish)
3. [Secure the starting point](#lesson-3--secure-the-starting-point)
4. [Set up your laptop: Python, VS Code and Git](#lesson-4--set-up-your-laptop-python-vs-code-and-git)
5. [HTML, CSS and JavaScript foundations](#lesson-5--html-css-and-javascript-foundations)
6. [Build and understand the first Flask pages](#lesson-6--build-and-understand-the-first-flask-pages)
7. [Model OWASP Top 10 content with JSON](#lesson-7--model-owasp-top-10-content-with-json)
8. [Learn APIs with NVD fixtures and curl](#lesson-8--learn-apis-with-nvd-fixtures-and-curl)
9. [Normalise, cache and enrich CVEs](#lesson-9--normalise-cache-and-enrich-cves)
10. [Make the CVE explorer usable and safe](#lesson-10--make-the-cve-explorer-usable-and-safe)
11. [Test, debug and security-review](#lesson-11--test-debug-and-security-review)
12. [Deploy with Gunicorn, systemd and Nginx](#lesson-12--deploy-with-gunicorn-systemd-and-nginx)
13. [Present, evaluate and extend](#lesson-13--present-evaluate-and-extend)

Appendix A: [Challenge cards](#appendix-a--challenge-cards) · Appendix B: [Responsible AI assistance log](#appendix-b--responsible-ai-assistance-log)

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

### How your laptop, GitHub and Linode fit together

This project uses three separate machines, and it is important you understand the *shape* of that arrangement before you type a single command, because it explains almost every instruction later in this guide.

```text
Your laptop (VS Code)                 GitHub                          Linode server
┌───────────────────────┐  git push  ┌────────────────────┐ git pull ┌─────────────────────────┐
│ Edit HTML/CSS/JS/Python│ ─────────►│ Your PUBLIC         │─────────►│ gunicorn + Nginx run the │
│ Run "python app.py" to │           │ repository          │          │ real, live dashboard      │
│ preview changes locally│ ◄───────  │ (the only bridge     │          │ Reached only through the │
│ git commit             │  git pull │  between the other   │          │ browser-based LISH       │
└───────────────────────┘  (rare)    │  two machines)       │          │ console, never SSH        │
                                      └────────────────────┘          └─────────────────────────┘
```

* **Your laptop** is where all of your actual coding happens: writing HTML/CSS/JavaScript/Python in VS Code, running the Flask development server to preview your work, and running your automated tests. Nothing you do here is visible to anyone else until you push it.
* **GitHub** holds **your own public repository** — a copy of the project's history that both your laptop and your Linode server can talk to. It is the *only* connection between the other two machines. Your laptop never talks to the Linode server directly, and the Linode server never talks to your laptop directly.
* **Your Linode server** is a real cloud computer that hosts the finished, running dashboard for anyone on the internet to visit. You do not edit code here. You only pull down commits that already exist on GitHub, and use a small number of Linux commands to keep the service running.

**Why is there no direct connection between your laptop and the server?** Two reasons, one practical and one professional. Practically, your school/college network blocks outbound SSH, which is the normal way people connect a laptop directly to a cloud server — so a direct connection is not available to you even if you wanted one. Professionally, this "laptop → shared repository → server" pattern (sometimes summarised as **GitOps**) is exactly how real software teams operate: nobody securely copies files by hand onto a production server; instead, a trusted, reviewable history in a shared repository is what gets deployed. You are learning the pattern used by real engineering teams, not a workaround.

**Because you cannot SSH into the server, you will use LISH** — Linode's browser-based console, opened from the Linode Cloud Manager website over ordinary HTTPS (the same protocol as any web page), not over the SSH port your network blocks. Lesson 2 explains LISH fully.

**Because your GitHub repository is public**, treat every commit as something a stranger, a future employer, or an automated scanner could read within seconds of your push. `.env` files, API keys, passwords and personal information must never be committed — the `.gitignore` in this project already excludes `.env`, but it cannot protect you if you paste a secret directly into a tracked file. On the positive side, a clean, well-explained public repository with sensible commit messages is something you can genuinely show a future employer or apprenticeship interviewer — treat your commit history as part of the deliverable, not just the final code.

### Rules, choices and evidence

|Fixed core requirements|Your choices|
|---|---|
|Flask, NVD API, local OWASP JSON, safe output, tests, non-root deployment|Project name/logo text, accessible colour palette, OWASP layout, CVE card/table layout, summary metrics, priority order, one extension|

Keep a folder named `evidence` outside Git or a private classroom drive. Save command output, screenshots, test results, decision records and feedback there.

### Your invented practice dataset

Several lessons ahead reuse the same eight **invented** CVE records so you can compare your predictions against real behaviour without waiting for live data. These identifiers, products and flaws are made up for teaching. **Do not search for, report, scan for or attempt to exploit any of them — they do not correspond to real vulnerabilities.**

|ID|Short description|Published|CVSS score|Severity|Known exploited (KEV)|Example CWE|Best-fit OWASP category|
|---|---|---|---:|---|---|---|---|
|CVE-2026-90001|Northstar Archive Server 4 — the backup endpoint never checks who is asking|2026-03-01|9.8|CRITICAL|No|CWE-284|A01 Broken Access Control|
|CVE-2026-90002|BrightDesk Remote Support 7 — ships with an unchangeable default support password|2026-03-02|8.1|HIGH|Yes|CWE-798|A07 Identification and Authentication Failures|
|CVE-2026-90003|Comet Timetable Widget — shows a search term back to the page without escaping it|2026-03-03|5.4|MEDIUM|No|CWE-79|A03 Injection|
|CVE-2026-90004|Harbor Print Queue — print-job details are visible to any logged-in user, not just the owner; no CVSS score published yet|2026-03-04|Not scored|HIGH|No|CWE-200|A01 Broken Access Control|
|CVE-2026-90005|Lantern Chat Widget — bundles a messaging library with a fixed, known flaw|2026-03-05|6.5|MEDIUM|No|CWE-1104|A06 Vulnerable and Outdated Components|
|CVE-2026-90006|Anchor Payments Gateway — the administrator account has a weak, guessable password|2026-03-06|9.1|CRITICAL|Yes|CWE-287|A07 Identification and Authentication Failures|
|CVE-2026-90007|Driftwood CMS — the login form never locks out repeated failed attempts|2026-03-07|4.3|MEDIUM|No|CWE-307|A07 Identification and Authentication Failures (see note)|
|CVE-2026-90008|Pinehurst Backup Agent — fetches any URL a user supplies, with no allow-list|2026-03-08|7.2|HIGH|No|CWE-918|A10 Server-Side Request Forgery|

**Note on CVE-2026-90007:** CWE-307 is not one of the two example CWEs listed for A07 in `data/owasp_top_10.json`. That is normal — the file's `cwes` field is described as "examples", not an exhaustive list. A real OWASP category covers many weaknesses; a short teaching file can only show a couple of them.

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
Read the three **invented** records below, taken from your practice dataset above. They are teaching data, not real vulnerabilities and not instructions to attack anything.

|Question|CVE-2026-90001|CVE-2026-90002|CVE-2026-90006|
|---|---|---|---|
|CVSS severity|Critical, 9.8|High, 8.1|Critical, 9.1|
|CISA KEV status|Not listed|Listed as known exploited|Listed as known exploited|
|Product|Northstar Archive Server 4|BrightDesk Remote Support 7|Anchor Payments Gateway|
|Does the organisation use it?|No: asset list and software inventory show no installation|Yes: it is used on a public helpdesk server|Yes: it runs the public checkout|
|Internet exposure|Not applicable|Public login page is reachable|Public checkout page is reachable|
|Fix available?|Unknown|Vendor patch is available|No patch yet|
|First action|Record the result and confirm the inventory is current|Assign urgent investigation: confirm version, restrict exposure if appropriate, test/apply the vendor patch under change control|Assign urgent investigation: since no patch exists yet, look at compensating controls (force a password reset, restrict admin access by IP) while a fix is awaited|

A quick ranking by score alone would put 90001 first because 9.8 is larger than 8.1 or 9.1. A security team instead uses several signals. 90002 and 90006 both have a used product, public exposure and a known-exploited signal — but they need *different* first actions, because one has a vendor patch and the other does not. This is not an automatic rule: the team still checks its own systems, service importance, compensating controls and change window.

### Try the reasoning yourself
For each statement, decide whether it is **true**, **false**, or **not enough information**:

1. "CVE-2026-90001 is harmless because the organisation does not use it."
2. "CVE-2026-90002 is definitely being exploited on this organisation's server."
3. "A CVSS score tells us whether a patch will be easy to apply."
4. "CISA KEV is a useful prioritisation signal."
5. "Because CVE-2026-90006 has no available patch yet, it should be ignored until one exists."

**Answers:** 1 is *not enough information*: the inventory might be incomplete, so record the check. 2 is *false*: KEV means exploitation is known in the wider world, not necessarily on this server. 3 is *false*: CVSS is not a change-management measure. 4 is *true*, but it must be combined with local context. 5 is *false*: a missing patch means the team investigates compensating controls sooner, not later.

## Tasks
1. Write an audience statement: "This dashboard helps ___ decide ___ because ___."
2. Draw the home page on paper. Include a title, four number cards, severity bars, a "look first" explanation, and a recent-CVE list.
3. Pick a name, font style and two main colours. Use an online contrast checker or browser DevTools to check text contrast. Do not use colour alone to mean "critical". (You will apply this properly in Lesson 5.)
4. Complete a decision record for your OWASP layout: cards, accordion, table/detail panel, or vertical timeline. The reference app uses cards; changing it is an extension after the core works.
5. Using the practice dataset table in section 0, decide a priority order for all eight records and write one sentence justifying your top choice. There is no single correct order — the mark is in the reasoning.

## Checkpoint and reflection
Show the sketch and decision record. Explain: "Why might a high CVSS score not be first priority?"
**Common mistake:** saying KEV means every organisation is affected. It means there is exploitation evidence, not that your systems are vulnerable.

**Stretch:** write a 50-word explanation of Vulnerability Dashboard for a non-specialist school governor.

---

# Lesson 2 — Linux foundations: connect to your Linode server with LISH
**Effort:** substantial. **Suggested Git checkpoint:** `record server orientation`.

## Why this matters
A cloud instance is a remote virtual computer rented from a provider — in this project, **Linode**. You control it through a terminal. Normally that terminal reaches the server over SSH, but your school/college network blocks outbound SSH connections, so you will connect a different way: through **LISH**, a browser-based console built into the Linode dashboard. Treat the server like a real production system regardless of how you reach it: use named users, record changes and avoid unnecessary exposure. Everything in this lesson is a skill you will reuse every remaining lesson, so it is worth doing slowly.

## New words
* **Linode Cloud Manager:** the website (`cloud.linode.com`) where you manage your Linode server: power it on/off, view its IP address, reset its root password, and open its console.
* **LISH (Linode Shell):** a console built into the Linode Cloud Manager that connects you to your server as if you had plugged a screen and keyboard directly into it. It works entirely over your normal browser connection (HTTPS, the same protocol as any web page), so it is unaffected by SSH being blocked. It also does not depend on the server's own network settings or firewall working correctly — even if you misconfigure networking on the server, LISH still gets you back in.
* **Weblish:** the specific text-based, browser-window version of LISH you will use (Linode also offers a graphical version called Glish, which you do not need for this headless server).
* **public IP address:** an address that can be reached from the internet; a **private IP address** is for internal networks only.
* **root:** the single most powerful account on a Linux system, able to do anything. You use it briefly to set up your own account, then avoid it for daily work.
* **user:** an account with its own files and permissions.
* **sudo:** "run this command with administrator privileges". It is powerful, not a shortcut.
* **shell:** the program that reads the commands you type, one line at a time, and runs them.
* **path:** the route to a file. An **absolute path** starts at `/`, the top of the filesystem, e.g. `/home/ubuntu/notes.txt`. A **relative path** starts from where you currently are, e.g. `notes.txt`. `~` is a shortcut for your home folder.

## 2.1 Open LISH and log in
1. Sign in to the Linode Cloud Manager at `cloud.linode.com` using the account details from your course setup record.
2. Open your Linode instance from the list, and note its **public IP address** shown on the summary page — you will need it in later lessons.
3. Click the **Launch LISH Console** button (sometimes shown as a "Console" tab). This opens Weblish in a new browser tab: a terminal window running entirely inside your browser.
4. If this is the first time anyone has logged in, you will see a `login:` prompt. Because LISH behaves like a screen plugged directly into the machine, it always asks for a **username and password** — key-based login, which is how SSH normally works, does not apply here. Log in as `root` using the root password from your course setup record. If you do not have one, use the Cloud Manager's **Reset Root Password** option, then reboot the Linode and try again.

**A note on copy and paste:** Weblish is a normal browser window, so you can usually paste multi-word commands using your browser's own paste shortcut (`Ctrl+Shift+V` on Windows/Linux, `Cmd+V` on macOS, or right-click → Paste) rather than retyping everything by hand. There is, however, **no file upload or drag-and-drop** into LISH — it is a keyboard-and-screen console, nothing more. Every file that ends up on this server will arrive either because you typed it directly, or because you ran `git pull` to fetch something already pushed to GitHub (Lesson 12). Keep this in mind: it is the reason secrets on the server later have to be typed in by hand rather than copied across as a file.

## 2.2 Create your own account — do not stay logged in as root
Working as `root` for anything beyond initial setup is unsafe: one mistyped command has no safety net. Create yourself a normal account with `sudo` privileges, then use that from now on.

```bash
adduser YOUR-NAME
usermod -aG sudo YOUR-NAME
su - YOUR-NAME
whoami
```

`adduser` creates the account and asks you to set a password — choose a strong one you have not used elsewhere, since it is the only credential protecting this console. `usermod -aG sudo` adds you to the `sudo` group, so you can still run administrator commands when needed by typing `sudo` first. `su - YOUR-NAME` switches into your new account inside the same LISH session; `whoami` confirms you are no longer `root`. From this point on, log in to LISH as `YOUR-NAME`, not `root`, and use `sudo` only for the specific commands that need it.

**Checkpoint:** you can log out of LISH entirely (close the tab) and reopen it, logging in as your own user with your own password, not root.
**Common mistake:** doing all remaining work logged in as `root` "because it's easier". Every remaining lesson assumes a named, least-privilege user; root is for emergencies and initial setup only.

## 2.3 Lab: paths, folders and files
A computer stores files inside folders (also called directories). Try this on the server, one line at a time:

```bash
pwd
mkdir -p ~/dashboard-lab/week1
cd ~/dashboard-lab/week1
pwd
ls -la
touch first-note.txt
ls -la
```

`touch` creates an empty file if it does not exist, or updates its timestamp if it does. `mkdir -p` makes all missing folders in a path and does not complain if they already exist. In the output of `ls -la`, the first character `d` means directory and `-` means ordinary file; `.` means the current folder and `..` means the parent.

### Guided challenge
1. Create `~/dashboard-lab/week1/assets`, enter it with `cd`, and prove your location with `pwd`.
2. Create `colours.txt` with `touch`, then go back one folder with `cd ..`.
3. List the contents of `assets` without entering it: `ls -la assets`.
4. Copy `first-note.txt` to `copy.txt` with `cp`, then rename it to `moved.txt` with `mv`.
5. Return home with `cd` on its own. Why does this work from any starting folder?
6. Clean up only your practice folder: `rm -r ~/dashboard-lab/week1/assets`. `rm -r` permanently deletes a folder and its contents. Run `pwd` first and type the full path; never use it with a path you do not understand.

**Checkpoint:** you can explain absolute, relative and home-folder paths, and what `cp` does differently from `mv`.
**Try a mistake safely:** type `cd missing-folder`. Read the error, then run `ls` to see why it failed. Do not create a random folder just to silence an error.

## 2.4 Lab: read and edit text safely
Configuration and code are text files. A command-line editor does not protect you from mistakes, so make one change, save, inspect, then continue. `nano` is a good choice because its shortcuts appear at the bottom of the screen.

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
1. Add a fourth line with `nano`, then search it: `grep -n 'word-you-used' first-note.txt`. `-n` adds line numbers.
2. Print only the final two lines: `tail -n 2 first-note.txt`.
3. Compare file listings with `ls -l` before and after editing.

**Checkpoint:** explain the difference between copying and moving a file.
**Common error:** saving a file in the wrong folder. Use `pwd` before `nano`, or use an absolute path.

## 2.5 Lab: permissions in plain English
Linux permissions decide who may read (`r`), write (`w`) or enter/execute (`x`) a file. `ls -l` shows three groups: owner, group, everyone else. A private key should not be readable by everyone. Do not solve every problem with `sudo` or `chmod 777`; that hides the question "who should really have access?"

```bash
cd ~/dashboard-lab/week1
ls -l first-note.txt
chmod 600 first-note.txt
ls -l first-note.txt
```

`600` means owner can read/write; group and others have no permissions. This is appropriate for a private text note, not necessarily a shared web asset. Restore a normal readable example with `chmod 644 first-note.txt` (owner read/write; others read).

**Checkpoint:** explain why a service account needs read permission to application files but should not own system configuration. You will use this idea again in Lesson 3 and Lesson 12.
**Safety rule:** only change permissions on files you own in this lab. Record the old mode before changing a production file.

## 2.6 Lab: reading command help
Good developers do not memorise every option. They find help, read the relevant part, and test a small example. On Ubuntu, `man` opens a manual page, `--help` gives short help, and `apropos` searches manual titles.

```bash
mkdir --help | less
man ls
apropos 'copy files'
```

Quit a manual with `q`. Look up `cp` and identify what recursive copying means before you ever use `cp -r`. Do not run options merely because an example contains them.

## 2.7 Full command reference

|Command|Purpose|Example|What to look for|
|---|---|---|---|
|`pwd`|print current folder|`pwd`|Usually `/home/ubuntu`|
|`ls -la`|list files, including hidden ones|`ls -la`|`.` means current; `..` parent|
|`cd NAME`|enter a folder|`cd projects`|Prompt/folder changes|
|`cd ..`|go up one level|`cd ..`|Useful after a mistake|
|`mkdir -p NAME`|make a folder (and parents)|`mkdir -p practice/notes`|New folders appear in `ls`|
|`cp A B`|copy file|`cp notes.txt notes-copy.txt`|Both files exist|
|`mv A B`|move/rename|`mv notes-copy.txt old-notes.txt`|Old name disappears|
|`cat FILE`|print small file|`cat notes.txt`|Use only for short text|
|`less FILE`|read long file|`less /etc/ssh/sshd_config`|`q` quits|
|`nano FILE`|simple terminal editor|`nano notes.txt`|`Ctrl+O`, Enter saves; `Ctrl+X` exits|
|`grep TEXT FILE`|find text|`grep -n 'Port' /etc/ssh/sshd_config`|`-n` includes line numbers|
|`tail -n 30 FILE`|last lines of a file|`tail -n 30 /var/log/...`|Useful for new log entries|
|`chmod MODE FILE`|change permissions|`chmod 600 key.pem`|`ls -l` shows the new mode|
|`whoami` / `id`|current user/permissions|`id`|Shows groups|
|`ps aux`|running processes|`ps aux \| grep gunicorn`|A pipe sends output to grep|
|`ss -tulpn`|list listening network ports|`sudo ss -tulpn`|Check what is reachable|
|`systemctl`|manage services|`systemctl status nginx`|Does not edit files|
|`journalctl`|read service logs|`journalctl -u nginx -n 30`|`-u` selects a service|
|`curl`|make an HTTP request|`curl -I http://127.0.0.1`|`-I` asks for headers|
|`man` / `--help`|read documentation|`man cp`|`q` to quit a manual|

## Checkpoint
Run `whoami`, `id`, `ss -tulpn`, and `systemctl status ssh --no-pager`. A pager lets long output scroll; `--no-pager` prints it once. Explain which command tells you your current folder and which command tells you your identity. Notice that `sshd` (the SSH server) is running by default even though you never use it to log in yourself — you will decide what to do about that in Lesson 3.

**Likely errors:** `No such file or directory` usually means the folder/file spelling is wrong; use `pwd` and `ls`. `Permission denied` means your user cannot perform that action; do not automatically add `sudo` — ask why permission is needed. If LISH itself appears frozen or shows a blank screen, try pressing Enter, resizing the browser window, or closing and reopening the console tab from the Cloud Manager — this is a display quirk of the browser terminal, not a problem with the server.

---

# Lesson 3 — Secure the starting point
**Effort:** medium. **Suggested Git checkpoint:** `document basic server hardening`.

## Why this matters
A public server receives internet traffic. Least privilege means each user and service has only the access it needs — the same idea you practised with `chmod` in Lesson 2.5, now applied to whole accounts and network ports. Do hardening one small reversible step at a time. You have an unusual safety net here: because you connect through **LISH**, not SSH, nothing you do to the network stack, the firewall, or `sshd` can ever lock you out of the box — LISH bypasses all of it. That does not mean carelessness is fine; it means you can practise real hardening discipline (verify, then apply) without the classic fear of a broken SSH session stranding you.

## Tasks with verify and undo steps
1. **Update the operating system.**
   ```bash
   sudo apt update
   sudo apt upgrade
   ```
   `apt update` downloads a list of available package versions. `apt upgrade` installs updates. Verify that it finishes without errors. Undoing package updates is not usually simple; take a Linode snapshot or backup first if available.
2. **Create the application account.**
   ```bash
   sudo adduser --system --group --home /srv/vulnerability-dashboard vulnerability-dashboard
   id vulnerability-dashboard
   ```
   This makes a non-login system user and group for the service. Verify its UID/group using `id`. If created in error before deployment, you can remove it with `sudo deluser --remove-home vulnerability-dashboard`.
3. **Review SSH, even though you do not use it yourself.** By default Ubuntu runs `sshd`, reachable from the whole internet, whether or not you personally log in that way. Anyone scanning the internet can find it, so it is still your responsibility to secure or restrict it.
   ```bash
   sudo less /etc/ssh/sshd_config
   sudo sshd -t
   ```
   Look for `PasswordAuthentication` and `PermitRootLogin`. `sshd -t` checks syntax without applying changes. In a normal SSH-based deployment you would now open a second terminal to confirm you are not about to lock yourself out before reloading; here, LISH already gives you that guarantee, so apply the change directly: `sudo systemctl reload ssh`.
4. **Set the host firewall carefully.**
   ```bash
   sudo ufw allow OpenSSH
   sudo ufw status numbered
   sudo ufw enable
   sudo ufw status verbose
   ```
   UFW is Ubuntu's own firewall tool, enforced inside the server. Allowing `OpenSSH` here still matters — it is a record of intent and keeps the option open for legitimate admin tools — even though you personally never connect that way. Verify rules and status. Undo a specific accidental rule with `sudo ufw delete NUMBER`, using the number shown; emergency undo is `sudo ufw disable`, and record the change. Unlike a normal server, disabling UFW entirely by mistake here would not lock you out of anything, since LISH is unaffected — but still treat it with production-level care.
5. **Inspect ports.** Run `sudo ss -tulpn`. At this stage, only services you expect should listen. Later, allow Nginx HTTP/HTTPS rather than opening Gunicorn's internal port.
6. **Add a second, independent layer: the Linode Cloud Firewall.** UFW runs *inside* the server; a Linode Cloud Firewall is enforced *outside* it, at Linode's own network edge, before traffic ever reaches your Linode at all. In the Linode Cloud Manager, open **Firewalls** → create a new firewall → attach it to your Linode. Add inbound rules allowing TCP 80 and 443 (you will need these from Lesson 12 onward). Because you only ever access this server through LISH, you have no legitimate use for external SSH — **explicitly deny inbound TCP port 22** in the Cloud Firewall rules, or simply do not allow it. This is a real, professional "defence in depth" decision: two independent layers (Cloud Firewall and UFW) must both agree before a port is reachable from the internet, and you have removed a whole avenue of attack that you never needed in the first place.

## Reflection
Why is running Gunicorn as `root` a poor choice? Why is it safe to be more aggressive about closing port 22 here than it would be on a server you normally reach over SSH?
**Stretch:** write a one-paragraph change record with purpose, command, verification and rollback for one firewall change, and explain in it which layer (UFW or Linode Cloud Firewall) would have stopped a given unwanted connection.

---

# Lesson 4 — Set up your laptop: Python, VS Code and Git
**Effort:** substantial. **Suggested Git checkpoint:** `initial project structure`.

## Why this matters
From here on, almost everything you build happens on **your own laptop**, not on the Linode server. You write and test code locally, using an editor called VS Code, and you use Git to record and share your work through your own **public** GitHub repository. The Linode server, which you only ever reach through LISH, will not run Python or Flask directly until Lesson 12 — until then, it stays a plain Ubuntu box you occasionally revisit for Linux practice.

Throughout the rest of this guide, commands are written for a typical terminal. Where macOS/Linux and Windows commands genuinely differ, both are shown; otherwise, wherever you see `python`, macOS/Linux users should read this as `python3` if plain `python` is not recognised or reports Python 2.

## 4.1 Install VS Code, Python and Git on your laptop
1. **VS Code:** download and install it from `code.visualstudio.com` for your operating system. Open it once to confirm it starts.
2. **Python:**
   * **Windows:** download the installer from `python.org/downloads`, run it, and **tick "Add python.exe to PATH"** before clicking Install — this single checkbox is the single most common source of "python is not recognised" errors. Open a **new** PowerShell/terminal window afterwards (existing windows will not see the update) and check: `python --version`.
   * **macOS:** install from `python.org/downloads`, or with Homebrew (`brew install python3`) if you have it. Check with `python3 --version`.
   * **Linux:** `sudo apt install -y python3 python3-venv python3-pip`, then check with `python3 --version`.
3. **Git:**
   * **Windows:** install "Git for Windows" from `git-scm.com`. Accept the default options during setup — they include a credential helper that will make GitHub sign-in far simpler later in this lesson.
   * **macOS:** `git --version` in Terminal will usually prompt you to install Apple's Command Line Tools, which include Git; accept the prompt.
   * **Linux:** `sudo apt install -y git`.
4. In VS Code, open **View → Terminal** to get an integrated terminal, and install the **Python** extension (Microsoft) from the Extensions panel (the icon of four squares in the sidebar) — it gives you syntax highlighting, linting and a "Run Python File" button for the work ahead.

**Checkpoint:** running `python --version` (or `python3 --version`), `git --version` and opening VS Code's integrated terminal all work without errors.
**Likely error:** `'python' is not recognized as an internal or external command` on Windows almost always means the PATH checkbox was missed during install — reinstall and tick it, or add Python to PATH manually, then open a brand-new terminal window.

## 4.2 Create your GitHub account and your public repository
1. If you do not already have one, create a free account at `github.com`. Use an email address you will still have access to after this course.
2. Create a new **public** repository for your dashboard. If your tutor has provided a starter/template repository, use GitHub's "Use this template" button to generate your own independent public copy of it; otherwise create an empty public repository and you will populate it in the next step. Give it a sensible name, e.g. `vulnerability-dashboard`.
3. Read the short description GitHub gives you for "public" versus "private" before you confirm — you are deliberately choosing **public**, so any of your commits are visible to anyone on the internet. Revisit section 0's note on why that matters (never commit secrets; keep it as a portfolio piece).

### Authenticating with GitHub: why not SSH keys?
Pushing to GitHub normally needs either an SSH key or a **Personal Access Token (PAT)** used over HTTPS. This project uses **HTTPS with GitHub's sign-in flow**, for two reasons: it needs no key-pair setup, and — usefully, given your network blocks SSH generally — it works entirely over ordinary HTTPS (port 443), the same as browsing the web. When VS Code's Source Control panel first asks you to push, click **Sign in with GitHub**; a browser tab opens for you to authorise VS Code, and your credentials are then stored securely by your operating system's credential manager (Windows Credential Manager, macOS Keychain, or the Git Credential Manager installed alongside Git). You will not need to type a password or token again on this laptop.

If you ever need the manual fallback (for example, a script or an unusual terminal that cannot open a browser), GitHub can issue a **Personal Access Token**: a long random string that acts like a password with a limited scope and expiry date, created under GitHub Settings → Developer settings → Personal access tokens. Treat a PAT exactly like a password — never commit it, never paste it into chat, and revoke it immediately if you ever expose it by accident.

## 4.3 Clone your repository to your laptop
Choose or create a folder for your coursework — for example a `projects` folder inside your home folder/Documents — then clone your **own** repository into it (not the original class reference repository):

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/vulnerability-dashboard.git
cd vulnerability-dashboard
```

Using `https://` (not `git@`) means Git will authenticate over HTTPS using the sign-in flow from 4.2, rather than expecting an SSH key. Open the folder in VS Code: `code .` from the terminal, or File → Open Folder.

Set your identity once, so your commits are correctly attributed to you rather than a generic placeholder:
```bash
git config --global user.name "Your Name"
git config --global user.email "the-email-you-used-for-github@example.com"
```

## 4.4 Create your virtual environment and run the tests
A **virtual environment** (`venv`) is an isolated folder containing Python packages for one project, so installing a package here never affects another project or your operating system's own Python.

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```
**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

Your prompt should now start with `(.venv)`. Leave the environment later with `deactivate`. If `pip` installs but Python cannot import Flask, check whether the prompt still shows `(.venv)` — you may have opened a new terminal tab that needs activating again.

**Windows-specific error:** `cannot be loaded because running scripts is disabled on this system` when activating means PowerShell's execution policy is blocking the activation script. Run `Set-ExecutionPolicy -Scope Process Bypass` in that same PowerShell window and try activating again — this only relaxes the policy for the current window, not your whole system.

Confirm everything works before writing any code of your own:
```bash
pytest -q
python app.py
```
Open `http://127.0.0.1:5000` in your own browser — this is now running entirely on your laptop, with nothing published anywhere else yet. Stop it with `Ctrl+C`.

**A note on two separate environments:** you will create a *second*, completely independent virtual environment later, on the Linode server, when you deploy in Lesson 12. They share nothing except the same `requirements.txt`/`requirements-dev.txt` files tracked in Git — installing a package here never affects the server, and vice versa. This is normal and expected, not a mistake to "fix" by trying to share one environment between two machines.

## 4.5 Python fundamentals, using your practice dataset
You will read and adapt real Python throughout this project. Before that, build the vocabulary using a scratch file. In VS Code, create a new file called `python_basics.py` somewhere outside your Git project (for example in a `dashboard-lab` folder next to it, so it is never accidentally committed), and work through it a section at a time. Use VS Code's **Run Python File** button (the triangle in the top right of the editor, provided by the Python extension) or a terminal command — `python python_basics.py` (Windows) / `python3 python_basics.py` (macOS/Linux) — after each addition.

### Variables, types and f-strings
```python
identifier = "CVE-2026-90001"      # a string
score = 9.8                        # a float (a number with a decimal point)
is_known_exploited = False         # a boolean: True or False
weakness = None                    # Python's "no value yet"

print(f"{identifier} scored {score}")
```
`f"..."` is an **f-string**: anything inside `{}` is evaluated and inserted. `None` is not the same as `0` or `False` — it means "nothing has been supplied", which is exactly how the dashboard represents a missing CVSS score.

### Lists and dictionaries
A **list** is an ordered collection written with `[]`. A **dictionary** (`dict`) maps named keys to values, written with `{}` — the same shape as a JSON object you will meet in Lesson 7.

```python
cves = [
    {"id": "CVE-2026-90001", "severity": "CRITICAL", "score": 9.8, "known_exploited": False},
    {"id": "CVE-2026-90002", "severity": "HIGH", "score": 8.1, "known_exploited": True},
    {"id": "CVE-2026-90004", "severity": "HIGH", "score": None, "known_exploited": False},
]

print(cves[0])            # the first item: position 0, not 1
print(cves[0]["severity"]) # "CRITICAL"
print(cves[0].get("cvss_version"))  # None: .get() never crashes on a missing key
```
Square brackets `cves[0]` select a list position. `dictionary["key"]` raises an error (`KeyError`) if the key is absent; `dictionary.get("key")` returns `None` instead. External data is often incomplete, so the real application almost always uses `.get`.

### Loops and conditionals
```python
for cve in cves:
    if cve["score"] is None:
        print(f"{cve['id']}: not scored yet")
    elif cve["severity"] == "CRITICAL":
        print(f"{cve['id']}: investigate soon")
    else:
        print(f"{cve['id']}: {cve['severity']}")
```
`for item in list:` runs the indented block once per item. `if` / `elif` / `else` chooses one branch. Indentation is not decoration in Python — it defines which lines belong to the loop or the branch.

### Functions
```python
def count_by_severity(cves, target_severity):
    total = 0
    for cve in cves:
        if cve["severity"] == target_severity:
            total += 1
    return total

print(count_by_severity(cves, "HIGH"))  # 2
```
`def` starts a function definition; the values in brackets are **parameters**; `return` sends a value back to the caller. Predict the answer before you run it, then check.

### From a loop to a comprehension
The loop above can be written as a **list comprehension** — a compact way to build a list from another list:

```python
high_severity_ids = [c["id"] for c in cves if c["severity"] == "HIGH"]
print(high_severity_ids)  # ['CVE-2026-90002', 'CVE-2026-90004']

how_many_high = sum(1 for c in cves if c["severity"] == "HIGH")
print(how_many_high)  # 2
```
`[expression for item in list if condition]` reads as "build a new list from `expression`, for each `item` in `list`, but only where `condition` is true". `sum(1 for ... if ...)` is the same idea used to count instead of collect. This pattern is exactly what you will find inside `services/normalisers.py` in Lesson 9 — it will already look familiar.

One more building block you will meet there: `next(generator, default)` takes the **first** value a generator produces, or a fallback if there are none at all:

```python
first_high = next((c["id"] for c in cves if c["severity"] == "HIGH"), "none found")
print(first_high)  # 'CVE-2026-90002'
```

### Guided task
1. Using the full eight-record practice dataset from section 0, write it out as a Python list of dictionaries in your scratch file (only the `id`, `severity`, `score` and `known_exploited` fields are needed).
2. Write a function `count_exploited(cves)` using a plain loop, run it, and check the answer against your own count of the table (should be 2).
3. Rewrite the same count as a comprehension/`sum(...)` expression and confirm you get the same answer.
4. Write one line using `next(...)` that finds the `id` of the first CRITICAL record, with a sensible fallback string if none existed.

**Checkpoint:** you can explain, in your own words, what a list comprehension does and why `.get()` is safer than `["key"]` for data that might be incomplete.

## 4.6 Git guided tasks
You already cloned your repository and set your identity in 4.3. `.gitignore` tells Git which local files, such as `.env`, must never be added — worth double-checking now that everything you push is public.

```bash
git status
git add README.md
git commit -m "Explain project purpose"
git log --oneline
git diff
git switch -c improve-readme
# make one small documentation change
git add README.md && git commit -m "Clarify local setup"
git switch main
git merge improve-readme
git push
```
`git status` answers "what changed?"; `git add` chooses changes for the next snapshot; `git commit -m` records them with an explanation; `git diff` shows unstaged changes; `git push` sends your commits to your public GitHub repository — this is the moment they stop being private to your laptop. If your default branch is not `main`, run `git branch --show-current` and substitute it.

**VS Code alternative:** every command above has a matching button in the **Source Control** panel (the icon with branching lines in the sidebar): a `+` to stage a file, a message box and tick to commit, a "Sync Changes" button that pushes and pulls together, and a graphical diff view when you click a changed file. Both routes do the same thing underneath — use whichever is faster for you, but make sure you can still explain what each button actually does in Git terms.

### Worked example: a small, recoverable change
Imagine `git diff` shows only one added sentence. Committing, pushing and reviewing it looks like this:
```bash
git status
git diff
git add templates/index.html
git commit -m "Add dashboard audience statement"
git push
git log --oneline -3
```
If `git status` unexpectedly lists `.env`, stop: it must not be staged, let alone pushed to a public repository.

Now practise recovering from an unwanted commit:
```bash
git log --oneline -1
git revert HEAD
git push
git log --oneline -2
```
`git revert` creates a **new** commit that reverses the previous one — safer for shared history than editing old commits. Refresh the page to confirm the text returned to its earlier state. Note that the original, unwanted commit is still visible in your public history after a revert — reverting undoes its *effect*, not its *existence*. This is exactly why secrets must never be committed in the first place: there is no equivalent "revert" that makes a leaked secret unseen.

### Controlled merge-conflict exercise
In a pair, both edit the same single sentence differently in separate branches, and both push your branches to your own repository (or to a shared practice repository your tutor sets up, if working across two GitHub accounts). Merge one branch, then merge the other. Git places conflict markers. Read both versions, keep the intended text, remove the markers, `git add`, and commit — VS Code's Source Control panel will highlight conflicted files and offers an inline "Accept Current/Incoming/Both" tool if you would rather resolve it visually than by reading raw markers. Tag this practice milestone with a name that will not be confused with your real release later: `git tag -a v0.1-practice-merge -m "First classroom merge-conflict practice"` then `git push --tags`. The real release tag, `v1.0.0`, is reserved for Lesson 12 when the dashboard is actually deployed.

**Never:** add `.env`, `*.pem`, downloaded keys or copied server secrets. Check `git status` before every `git add .`, and remember that `git push` is the point of no return for anything sensitive — once it is public, treat any exposed secret as compromised and rotate it immediately rather than trying to hide it with another commit.

---

# Lesson 5 — HTML, CSS and JavaScript foundations
**Effort:** substantial. **Suggested Git checkpoint:** `build a standalone practice page`.

## Why this matters
Before you edit the dashboard's real templates, build a small page entirely by hand, on your laptop, in VS Code. This is the only way to get real practice writing markup, styling it and adding behaviour, rather than only ever reading someone else's finished file. Work in a `dashboard-lab/webpage/` folder outside your Git project, so this practice page never becomes part of your dashboard's history.

## 5.1 HTML: structure first
HTML describes the **structure** and **meaning** of a page, not its appearance. In VS Code, create `dashboard-lab/webpage/practice.html`:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Practice CVE page</title>
  <link rel="stylesheet" href="practice.css">
</head>
<body>
  <header>
    <nav aria-label="Practice navigation">
      <a href="#top">Practice page</a>
    </nav>
  </header>

  <main id="top">
    <h1>Practice CVE list</h1>
    <p>This page is a local practice exercise, not part of the real dashboard.</p>

    <section aria-label="Search">
      <label for="search">Search records</label>
      <input id="search" type="search" aria-describedby="search-help">
      <p id="search-help">Type part of an identifier or description.</p>
    </section>

    <section aria-label="Practice CVE cards">
      <article class="card">
        <h2><a href="#">CVE-2026-90001</a></h2>
        <p>Northstar Archive Server 4 — the backup endpoint never checks who is asking.</p>
        <p><span class="badge severity-critical">CRITICAL</span> Score: 9.8</p>
      </article>
      <article class="card">
        <h2><a href="#">CVE-2026-90002</a></h2>
        <p>BrightDesk Remote Support 7 — ships with an unchangeable default support password.</p>
        <p><span class="badge severity-high">HIGH</span> Score: 8.1 <span class="badge kev">Known Exploited</span></p>
      </article>
    </section>
  </main>

  <footer>
    <p>Practice page for learning HTML, CSS and JavaScript.</p>
  </footer>

  <script src="practice.js" defer></script>
</body>
</html>
```

Read each new element as you type it: `<header>`, `<nav>`, `<main>`, `<section>` and `<footer>` are **semantic** elements — they describe what a part of the page *is*, which helps screen readers and search engines, not just browsers. `<label for="search">` is connected to `<input id="search">` by matching `for`/`id` values: click the label text and the input receives focus. `aria-describedby` links the input to an explanatory paragraph. Open the file directly in a browser (right-click `practice.html` in VS Code's file explorer → **Reveal in File Explorer/Finder** and double-click it, or use a "Live Preview"/"Live Server" VS Code extension for auto-refresh on save) to see it rendered before any CSS exists.

### Guided task
1. Add a third practice card using **CVE-2026-90006** from your dataset (Anchor Payments Gateway, CRITICAL, 9.1, Known Exploited).
2. Add one more semantic landmark: wrap the two sections above with meaningful `aria-label` text if you have not already, and check with DevTools that each heading level (`h1`, then `h2`) is used in order, not skipped.
3. View the page with images/CSS disabled (or before `practice.css` exists) and confirm the content still makes sense read top-to-bottom. This is what a screen reader broadly experiences.

## 5.2 CSS: presentation with a system
CSS controls appearance. A **selector** chooses elements; a **declaration** is a property/value pair. Create `dashboard-lab/webpage/practice.css`:

```css
:root {
  --ink: #172033;
  --bg: #f5f8fb;
  --card: #ffffff;
  --accent: #064b78;
  --focus: #e05a00;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font: 16px/1.5 system-ui, sans-serif;
  color: var(--ink);
  background: var(--bg);
}

header, footer {
  background: #102a43;
  color: #fff;
  padding: 1rem;
}

main {
  max-width: 900px;
  margin: auto;
  padding: 1rem;
}

a:focus, input:focus {
  outline: 3px solid var(--focus);
  outline-offset: 2px;
}

.card {
  background: var(--card);
  padding: 1rem;
  border-radius: .5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, .12);
  margin-bottom: 1rem;
}

.badge {
  display: inline-block;
  padding: .15rem .5rem;
  border-radius: .3rem;
  font-weight: bold;
  font-size: .85rem;
}

.severity-critical { background: #7d1520; color: #fff; }
.severity-high { background: #a94600; color: #fff; }
.kev { background: #4d146b; color: #fff; }

/* Cards sit side by side on wide screens, stacked on narrow ones. */
main section[aria-label="Practice CVE cards"] {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}

@media (max-width: 500px) {
  main { padding: .5rem; }
}
```

`--ink`, `--bg` and friends are **custom properties**: named values reused with `var(--name)`. Change one line and every rule using it updates together — this is exactly how the real dashboard's colour system works (you will meet it again in `static/css/styles.css`). `box-sizing: border-box` makes padding count *inside* an element's declared width, avoiding a common sizing surprise. The `grid-template-columns: repeat(auto-fit, minmax(240px, 1fr))` line means "as many 240px-or-wider equal columns as fit" — resize your browser and watch the cards reflow with no media query needed for that part. The `@media` rule only applies extra styling below 500px wide.

### Guided task: colour and type with a job
Reuse the reasoning from Lesson 1's design task, now with tools:
1. Pick a background, text and accent colour. Check the accent-on-background and text-on-background pairs with a contrast checker (browser DevTools "Accessibility" panel, or an online WCAG contrast checker) and aim for at least 4.5:1 for normal text.
2. Choose one readable body font. The fastest, most reliable choice is your operating system's own font stack (`system-ui, sans-serif`, as used above) — it needs no download and cannot fail to load. If you want a webfont, pick one and check its licence (for example on Google Fonts), and load only the weights you actually use.
3. In DevTools, open the Elements/Styles panel, click `.card`, and change `padding` from `1rem` to `2rem` live. Observe the effect, then refresh to discard the experiment — this is how you should explore CSS before editing a real file.
4. Confirm severity colour is never the *only* signal: each badge above also has text (`CRITICAL`, `HIGH`), not just a colour.

## 5.3 JavaScript: responding to the user
JavaScript runs in the browser and can read/change the page after it has loaded. Create `dashboard-lab/webpage/practice.js`:

```javascript
// Toggle a "more detail" panel and keep aria-expanded in sync,
// the same pattern the real dashboard uses for its mobile menu.
const firstCard = document.querySelector('.card');
const toggle = document.createElement('button');
toggle.textContent = 'Show more detail';
toggle.setAttribute('aria-expanded', 'false');
firstCard.append(toggle);

const detail = document.createElement('p');
detail.textContent = 'Weakness: CWE-284, Broken Access Control.';
detail.hidden = true;
firstCard.append(detail);

toggle.addEventListener('click', () => {
  const isOpen = !detail.hidden;
  detail.hidden = isOpen;
  toggle.setAttribute('aria-expanded', String(!isOpen));
  toggle.textContent = isOpen ? 'Show more detail' : 'Hide detail';
});
```

`const` creates a named value that cannot be reassigned. `document.querySelector('.card')` finds the first element matching that CSS selector — the same selector syntax you just used in CSS. `document.createElement` builds a new element in memory; `.append` adds it to the page. `addEventListener('click', () => { ... })` runs the arrow function every time the button is clicked. `aria-expanded` tells assistive technology whether the extra content is currently visible.

### Why `textContent`, never `innerHTML`, for untrusted data
An API description is data from *outside* your application. It may contain characters with special meaning in HTML. Compare:

```javascript
// Safe: the browser treats the value as plain text, whatever it contains.
detail.textContent = 'Words with <strong>angle brackets</strong> and & symbols.';

// Do not do this with external data: it asks the browser to parse HTML,
// so a description could inject real markup or scripts.
detail.innerHTML = 'Words with <strong>angle brackets</strong> and & symbols.';
```

Paste both lines separately into your `practice.js`, reload, and compare what appears on the page: the first shows the literal angle brackets as text; the second renders `<strong>` as actual bold markup. This is why `dashboard.js` in the real project always builds elements and sets `.textContent`. Jinja templates behave the same way by default: `{{ value }}` is escaped automatically, and you should never add `|safe` to text that came from an external API.

### Guided task
1. Add a second toggle button to your second practice card (BrightDesk), reusing the same pattern.
2. Open DevTools Console and check for errors after each change.
3. Test both buttons using only the keyboard: `Tab` to reach the button, `Enter` or `Space` to activate it. If focus is invisible, revisit your CSS `:focus` rule from 5.2.

## Checkpoint
Show `practice.html` rendered in a browser: three cards, working toggle buttons, visible keyboard focus, and a contrast-checked colour pair. Explain, without looking at your notes, the difference between `textContent` and `innerHTML`.

**Reflection:** why might a decorative display font be unsuitable for CVE identifiers or dense data tables?
**Common mistakes:** hiding focus outlines "because they look messy"; using colour with no accompanying text; nesting headings out of order (`h1` straight to `h3`).
**Stretch:** add a `prefers-color-scheme: dark` media query with a second colour set, and check both pairs for contrast.

---

# Lesson 6 — Build and understand the first Flask pages
**Effort:** substantial. **Suggested Git checkpoint:** `add first Flask pages`.

## What Flask, HTML and templates do
A web request has a **method** (for example GET), a **URL**, headers and a response. Flask maps a URL to a Python function called a **route**. The route calls a template. A Jinja template is HTML with safe placeholders such as `{{ name }}` — the same double-brace idea, layered on top of the plain HTML you wrote in Lesson 5. CSS controls appearance; JavaScript adds small browser behaviour, exactly as it did in your practice page.

## 6.1 One complete request, read slowly
When you type an address into a browser, the browser requests a resource. The server responds with a status, headers and a body. The page you see is not "inside" Flask: Flask sends HTML to the browser, then the browser separately requests the CSS and JavaScript files referenced in it — just like your practice page's `<link>` and `<script>` tags.

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

`GET` asks to read a resource. `/health` is the route. `200 OK` means the server completed the request successfully. `Content-Type: application/json` says the body is JSON, not HTML.

## 6.2 Run the reference application locally
On your laptop, with your virtual environment active:
```bash
python app.py
```
Open `http://127.0.0.1:5000`. `127.0.0.1` means "this computer only" — nobody else, not even someone else on your home Wi-Fi, can reach it. Do **not** run Flask's development server this way once you reach the Linode server in Lesson 12; a proper deployment is the whole subject of that lesson. Stop it with `Ctrl+C`.

### Lab: processes and ports
A **process** is a running program. A **port** is a numbered doorway used for network traffic. A browser normally uses 80 (HTTP) or 443 (HTTPS); this local Flask example uses 5000. With `python app.py` still running, open a **second** terminal (a second tab in VS Code's integrated terminal works well) and run:

**Windows (PowerShell):**
```powershell
netstat -ano | findstr :5000
curl -i http://127.0.0.1:5000/health
Get-Process -Name python
```
**macOS/Linux:**
```bash
ss -tulpn | grep 5000
curl -i http://127.0.0.1:5000/health
ps aux | grep '[p]ython app.py'
```
On Windows, `netstat -ano` lists connections with a process ID (PID) in the last column; match that PID against `Get-Process` or Task Manager. On macOS/Linux, the square brackets in the `ps` command stop `grep` from finding its own process in the list. Either way, return to the first terminal and press `Ctrl+C` — this sends an interrupt to the program. Run the port command again; it should no longer show port 5000.

**Checkpoint:** explain why Gunicorn will later bind to `127.0.0.1:8000` and Nginx, not Gunicorn, faces the public internet (Lesson 12).

### Practise the request/response cycle
```bash
curl -i http://127.0.0.1:5000/health
curl -i http://127.0.0.1:5000/not-a-page
curl -I http://127.0.0.1:5000/
```
The first should be 200. The second should be 404, meaning the route does not exist. The third uses `-I` for headers only — find `Content-Security-Policy`, `Referrer-Policy` and `X-Content-Type-Options`. A header is not a substitute for safe code, but it adds a browser-side layer of protection.

## 6.3 Read before editing
In `app.py`, find `@app.route("/")`. The `@` line is a **decorator**: it tells Flask which URL should call the function below it. In `templates/base.html`, find `{% block content %}`; child pages fill that named area. In `templates/index.html`, `{{ data.fetched_at }}` inserts a value and Jinja escapes text by default — the same escaping behaviour you saw JavaScript's `textContent` provide in Lesson 5.

## 6.4 Guided task: build your own route and template
This is the moment you write a brand-new Flask page from nothing, not just edit an existing one.

1. In `app.py`, add a small Python list near the top, using three records from your practice dataset:
   ```python
   PRACTICE_CVES = [
       {"id": "CVE-2026-90001", "description": "Northstar Archive Server 4 — the backup endpoint never checks who is asking.", "severity": "CRITICAL", "score": 9.8, "known_exploited": False},
       {"id": "CVE-2026-90002", "description": "BrightDesk Remote Support 7 — ships with an unchangeable default support password.", "severity": "HIGH", "score": 8.1, "known_exploited": True},
       {"id": "CVE-2026-90006", "description": "Anchor Payments Gateway — the administrator account has a weak, guessable password.", "severity": "CRITICAL", "score": 9.1, "known_exploited": True},
   ]
   ```
2. Add a new route function, near the other routes inside `create_app`:
   ```python
   @app.route("/practice")
   def practice():
       return render_template("practice.html", cves=PRACTICE_CVES)
   ```
3. Create `templates/practice.html`:
   ```jinja
   {% extends 'base.html' %}
   {% block content %}
     <h1>Practice CVE list</h1>
     <p>This page uses a small hand-written list, not live NVD data.</p>
     <div class="cve-list">
       {% for cve in cves %}
         <article class="cve">
           <h3>{{ cve.id }}</h3>
           <p>{{ cve.description }}</p>
           <p>
             <span class="badge severity-{{ cve.severity|lower }}">{{ cve.severity }}</span>
             Score: {{ cve.score }}
             {% if cve.known_exploited %}<span class="badge kev">Known Exploited</span>{% endif %}
           </p>
         </article>
       {% endfor %}
     </div>
   {% endblock %}
   ```
4. Restart `python app.py` and visit `http://127.0.0.1:5000/practice`. You should see your three cards, already styled by `styles.css` because you reused the same class names as the real dashboard.

Notice the parallels with Lesson 5: `{% for cve in cves %}` is Jinja's loop syntax, doing the same job as the JavaScript `.forEach` you will meet in Lesson 10; `{% if cve.known_exploited %}` mirrors the `if` statement from Lesson 4's Python; `{{ cve.severity|lower }}` applies a **filter** (`lower`) to a value before inserting it.

**Checkpoint:** `/practice` loads with three correctly styled cards and no traceback. Explain, in your own words, the path a request takes from typing the URL to seeing the card.

## 6.5 Guided small change to the real pages
1. Open `templates/index.html` in VS Code.
2. Under the introductory paragraph, type one sentence explaining your chosen audience. This is **your code/text**, not starter code.
3. Save, refresh the browser, then use browser DevTools: right-click the sentence → Inspect.
4. Change one CSS colour in `static/css/styles.css`, refresh, and use the DevTools Elements/Styles panel to see the applied rule.

### Deliberate experiments
**Experiment A:** change `/health` to a nonexistent URL in curl; notice `404`. **Experiment B:** deliberately remove a closing Jinja brace from `templates/practice.html`, reload, read the error locally, then restore it immediately. Production visitors receive a generic error page, not a traceback.

**Likely errors:** `Address already in use` means another process owns port 5000; use `netstat -ano | findstr :5000` (Windows) or `ss -tulpn | grep 5000` (macOS/Linux) and stop only your own process. `TemplateNotFound` usually means a wrong filename or folder — check `templates/practice.html` is spelled and placed exactly as referenced. A browser cache can hide CSS changes; hard refresh with `Ctrl+Shift+R`.

---

# Lesson 7 — Model OWASP Top 10 content with JSON
**Effort:** medium. **Suggested Git checkpoint:** `display OWASP teaching data`.

## Why local JSON?
JSON is a text data format using objects `{}` and lists `[]` — the same shape as the Python dictionaries and lists from Lesson 4. The project keeps OWASP material in `data/owasp_top_10.json`, rather than scraping a webpage every request. That makes lessons reliable and lets a maintainer review wording. The source file labels official summaries separately from student-friendly explanations.

## Reading JSON, one value at a time
JSON uses braces `{}` for an object: named values such as `"id": "A01:2021"`. It uses square brackets `[]` for an ordered list of objects. A comma separates items, and indentation only helps a human reader — it does not change the data. JSON uses `true`, `false` and `null`, not Python's `True`, `False` and `None`, though `json.loads` converts between them automatically.

Open the real file with `less data/owasp_top_10.json`. Find `edition`, `categories`, and inside one category: `id`, `name`, `explanation`, `example`, `impact`, `prevention`, `url` and `cwes`. Then check it is syntactically valid:
```bash
python -m json.tool data/owasp_top_10.json > /dev/null
echo $?
```
Exit code `0` means valid JSON. If invalid, Python prints a line/column. Go to that line and look for a missing comma, quote or bracket.

## Guided task: author a JSON file from scratch
Before touching the real content file, practise writing JSON yourself with lower stakes. Create `dashboard-lab/owasp-practice.json` and type these three **invented** teaching categories by hand (do not copy-paste):

```json
{
  "edition": "Classroom practice set (not a real OWASP release)",
  "categories": [
    {
      "id": "PRACTICE-01",
      "name": "Oversharing Error Messages",
      "explanation": "A page shows a full technical error to every visitor instead of a short, friendly message.",
      "example": "A mistyped web address returns a stack trace with internal file paths.",
      "impact": "Helps an attacker learn about your system's internals.",
      "prevention": "Show a generic message to visitors; log full detail only for developers."
    },
    {
      "id": "PRACTICE-02",
      "name": "Trusting Whatever the Browser Sends",
      "explanation": "The server assumes a value from a form or URL is already valid.",
      "example": "A page trusts a hidden price field instead of checking it on the server.",
      "impact": "A visitor can submit a value the design never expected.",
      "prevention": "Validate and re-check every value on the server, not only in the browser."
    },
    {
      "id": "PRACTICE-03",
      "name": "Never Expiring a Login",
      "explanation": "A logged-in session stays valid forever, even on a shared computer.",
      "example": "A shared library computer stays logged in to a student's account the next day.",
      "impact": "Someone else could use an account that should have expired.",
      "prevention": "Expire sessions after inactivity and give users a clear sign-out."
    }
  ]
}
```

1. Validate it: `python -m json.tool dashboard-lab/owasp-practice.json` (should print the file back out with no error).
2. Deliberately delete one comma between two fields, run the command again, and read exactly what Python reports. Note the line/column, then fix it.
3. Add a fourth invented category of your own, following the same shape, and validate again.

## Guided task on the real content
1. Visit `/owasp` and locate one category.
2. In the matching entry inside `data/owasp_top_10.json`, improve **one** student explanation in plain English. Keep the meaning accurate and do not invent a claim about OWASP.
3. Refresh `/owasp`; check the card, link text and keyboard tab order.
4. Add a decision record explaining why you retained cards or chose a different layout (see your Lesson 1 decision record).
5. Using the "Best-fit OWASP category" column from your practice dataset in section 0, check each mapping against the real `data/owasp_top_10.json` categories. Do you agree with all eight? Note any you would map differently and why.

### Maintenance process
Before a future update, read the official OWASP Top 10 project, record the date and edition, compare categories, update the local JSON and links, label any student-written text, validate JSON, test `/owasp`, ask another person to review, then commit with a clear message. Never scrape OWASP at runtime.

---

# Lesson 8 — Learn APIs with NVD fixtures and curl
**Effort:** substantial. **Suggested Git checkpoint:** `learn NVD API request`.

## API vocabulary
An **API** is an agreed way for programs to exchange information. An **endpoint** is an API URL. A **query parameter** adds a choice after `?`, for example `?resultsPerPage=1`. A **header** carries request metadata. A **status code** reports the result: 200 successful, 400 invalid request, 401/403 access issue, 404 absent, 429 rate limit, 500 server fault.

## Exercise A: make a small manual request
When network access is permitted, run:
```bash
curl -i 'https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=1'
```
`-i` includes response headers. Find the first `HTTP` status, `Content-Type`, then the JSON body. Do not repeatedly run it: unauthenticated NVD requests are rate limited. If the classroom network blocks it, use the saved fixture below — this is a valid offline learning route.

## Exercise B: inspect a saved response, one nested step at a time
NVD's JSON nests much deeper than the flat OWASP file from Lesson 7. Here is a small **invented** example of the same shape:

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
        "id": "CVE-2026-90004",
        "descriptions": [],
        "metrics": {}
      }
    }
  ]
}
```

Follow the first score with this route: root object → `vulnerabilities` list → first item `[0]` → `cve` object → `metrics` object → `cvssMetricV31` list → first item `[0]` → `cvssData` object → `baseScore`. This explains why API-handling code can look long even when the final displayed value is only `9.8`. Notice the second record has no score at all — `metrics` is an empty object — matching CVE-2026-90004 in your practice dataset, which really is unscored.

Now inspect the real fixture:
```bash
python -m json.tool tests/fixtures/nvd_sample.json | less
```
Find `CVE-2026-0001`, the English `description`, `published`, `baseScore`, and `baseSeverity`. `tests/fixtures` is controlled sample data, not live data.

### Practise with Python
Create `dashboard-lab/read_json.py`:
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
`json.loads()` turns JSON text into Python dictionaries and lists — the exact objects you practised building by hand in Lesson 4. Square brackets select a known key or list position. Run it from the project folder so the relative fixture path is correct.

**Experiment 1:** change `[0]` to `[1]` for the second record and observe the error when it has no description. Restore it. **Experiment 2:** print `payload["totalResults"]` and explain why this is easier — it sits directly inside the root object, with no list index needed.
**Likely error:** `KeyError` means a dictionary key is missing; `IndexError` means a requested list position is absent. Robust application code uses `.get` and fallback values where external data may be incomplete — exactly the reasoning behind Lesson 9's normaliser.

## Exercise C: request from Python
Read `services/nvd_client.py`. The important starter code is:
```python
response = requests.get(NVD_URL, params=parameters, headers=headers, timeout=timeout)
response.raise_for_status()
payload = response.json()
```
`requests.get` sends HTTP GET. `params` becomes query parameters safely. `timeout` prevents waiting forever. `raise_for_status` turns a bad HTTP status into an exception. `.json()` parses JSON. **Do not type an API key into this file.** The app reads `NVD_API_KEY` from an environment variable.

**Controlled experiments:** (1) in a scratch Python file, print `response.status_code` after a permitted one-record request; (2) set `timeout=0.001` only in a local experiment and observe the error handling, then restore it.
**Likely errors:** 429 means wait and use cache, not a loop; invalid JSON should be handled as unavailable data; 500 is usually upstream; a timeout may be network or service delay.

---

# Lesson 9 — Normalise, cache and enrich CVEs
**Effort:** substantial. **Suggested Git checkpoint:** `normalise cache and enrich CVEs`.

## Why a normalisation layer exists
NVD's full JSON is designed for many uses. Templates only need a small model. `services/normalisers.py` converts each record to `id`, `description`, dates, score, severity, CVSS version, CWEs, NVD URL and optional KEV details. It carefully handles missing English text, no score and no CWE. Do not pass an entire external response directly into templates.

Compare the shapes directly:

|Upstream concept|Possible NVD location|Internal dashboard value|
|---|---|---|
|Identifier|`cve.id`|`id`|
|English description|one item in `cve.descriptions`|`description`|
|Base score|one CVSS metric version|`score`|
|Severity|same metric|`severity`|
|Weakness names|nested `weaknesses` descriptions|`weaknesses` list|
|External link|built from identifier|`nvd_url`|

For CVE-2026-90001 from your practice dataset, the normalised result looks like this:

```python
{
    "id": "CVE-2026-90001",
    "description": "Northstar Archive Server 4 — the backup endpoint never checks who is asking.",
    "published": "2026-03-01T09:30:00.000",
    "last_modified": None,
    "score": 9.8,
    "severity": "CRITICAL",
    "cvss_version": "3.1",
    "weaknesses": ["CWE-284"],
    "nvd_url": "https://nvd.nist.gov/vuln/detail/CVE-2026-90001",
    "known_exploited": False,
    "kev_details": None,
}
```

For CVE-2026-90004 (Harbor Print Queue, not scored), the same function must produce `"score": None` and still label it sensibly rather than showing `0` or crashing — `None` is not zero, and an absent score is not "low risk".

## Read one function line-by-line
```python
metric = next((metrics[key][0] for key in (...) if metrics.get(key)), {})
score = cvss.get("baseScore")
```
This is the exact pattern you practised in Lesson 4.2: a generator expression inside `next(..., {})` takes the first available metric version, or safely falls back to an empty dictionary if none exist. `.get` returns `None` instead of crashing when a key is absent. This is starter code. Your task is to explain it in your own words in a comment or notebook, not rewrite it from memory.

## Cache concepts
A cache is a saved successful result. It improves speed and respects rate limits. `CACHE_TTL_SECONDS` decides how long data is **fresh** (default 30 minutes). After that, the app tries NVD. If NVD fails and old data exists, it shows **stale** cached data and a warning. `write_cache` writes a temporary file then replaces it so a crash does not leave half-written JSON. It never stores the API key.

Assume `CACHE_TTL_SECONDS=1800` (30 minutes):

|Time|What happens|What the user should see|
|---|---|---|
|09:00|NVD succeeds; 20 normalised records are written|"Last refreshed 09:00"; normal dashboard|
|09:10|Page reloads; cache is 10 minutes old|Same data quickly; no NVD request needed|
|09:31|Cache is 31 minutes old; NVD succeeds|New cache written; normal dashboard|
|10:02|Cache is 31 minutes old; NVD times out|Older records plus a clear "Showing older cached data" warning|
|10:05|No cache exists; NVD fails|Friendly unavailable-data message, not a traceback|

**Reflection:** why is "always show the last result with no warning" misleading? *Answer:* users could make a time-sensitive decision believing old data is current. Production systems handling many servers at once might use Redis or a database instead of a single file, because several servers need shared, managed storage — a file cache is deliberately simple for a single-server classroom deployment.

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
4. Run the cache test suite with extra detail to see the stale-fallback behaviour proven automatically:
   ```bash
   pytest -q tests/test_cache.py -vv
   ```
   Read the test before and after running it. Find the mock that deliberately makes NVD fail — this is safer than disabling a real network connection to test failure.
5. Set `CACHE_TTL_SECONDS=1` in your shell — `$env:CACHE_TTL_SECONDS=1` on Windows PowerShell, `export CACHE_TTL_SECONDS=1` on macOS/Linux — restart the app, wait two seconds, and disconnect/disable external access only on a non-production/local test environment. Observe the stale warning when upstream data cannot refresh. Restore the default by closing that terminal, or `Remove-Item Env:CACHE_TTL_SECONDS` (Windows) / `unset CACHE_TTL_SECONDS` (macOS/Linux).
6. Explain why the CISA client catches failures and still returns CVEs.

---

# Lesson 10 — Make the CVE explorer usable and safe
**Effort:** medium. **Suggested Git checkpoint:** `add search filters and accessible UX`.

## Browser filtering
The server supplies a normalised list. `static/js/dashboard.js` filters the list in the browser by search, severity, minimum score and KEV flag, then sorts it — using the same `Array.filter`/`Array.sort` idea as the toggle behaviour you built by hand in Lesson 5, just applied to a bigger dataset. This is suitable for a small teaching data set. Larger data needs pagination/server-side filtering.

### Critical security detail
Lesson 5 showed why `dashboard.js` creates elements and sets `.textContent` for CVE descriptions, never `.innerHTML`: API descriptions are external input, and `innerHTML` would let the browser interpret markup inside them. Keep this behaviour when you extend the file. Jinja also escapes `{{ values }}` by default.

## Predict the filters before you test them
Use your eight-record practice dataset from section 0 (reproduced here for convenience):

|ID|Severity|Score|Known exploited|
|---|---:|---:|---|
|CVE-2026-90001|CRITICAL|9.8|No|
|CVE-2026-90002|HIGH|8.1|Yes|
|CVE-2026-90003|MEDIUM|5.4|No|
|CVE-2026-90004|HIGH|not scored|No|
|CVE-2026-90005|MEDIUM|6.5|No|
|CVE-2026-90006|CRITICAL|9.1|Yes|
|CVE-2026-90007|MEDIUM|4.3|No|
|CVE-2026-90008|HIGH|7.2|No|

Write down your prediction for each before checking the answer:

1. Severity = HIGH → **90002, 90004, 90008** (three records).
2. Minimum score = 8.0 → **90001 (9.8), 90002 (8.1), 90006 (9.1)**; the not-scored record 90004 is not included.
3. Known Exploited only → **90002, 90006**.
4. Severity = HIGH **and** Known Exploited only → **90002 only**.
5. Severity = HIGH **and** minimum score = 9.0 → **no matches**; 90002 scores 8.1, 90004 has no score, 90008 scores 7.2. The empty-state message should explain what happened rather than showing a blank page.
6. Severity = CRITICAL → **90001, 90006**.

Load this same data into `/cves` (using the cache-population step from Lesson 9) and repeat each prediction against the real UI. Use **Clear filters** between attempts. If a result surprises you, read the values shown on each card before assuming the code is wrong.

## Guided tasks
1. Open `/cves`. Search an identifier, choose each severity, set a minimum score, tick KEV-only, change sort and press Clear filters.
2. Use Tab, Shift+Tab, Enter and Space only. Can you open navigation, use every form control and read the result-count update?
3. Use responsive mode in DevTools (or shrink the browser under 650px). Open and close Menu. Check text does not overlap and the focus outline is visible.
4. Add one plain-English empty-state sentence or improve an accessible label. Test it with a deliberately non-matching search.
5. Inspect `dashboard.js` and identify the line using `textContent`. Explain why a description containing angle brackets is displayed as text, rather than run as markup.

**Common mistakes:** hiding focus outlines; using red/green without words; changing `textContent` to `innerHTML`; assuming "not scored" means low risk.

---

# Lesson 11 — Test, debug and security-review
**Effort:** substantial. **Suggested Git checkpoint:** `test and security review`.

## What tests are
A test is repeatable evidence. **Arrange** creates inputs; **Act** calls code; **Assert** checks expected output. Unit tests check a small unit such as a normaliser. Route tests check Flask responses. Fixtures provide predictable data. Mocks replace a live dependency to simulate timeout/failure. Tests must not depend on a live public API because its data/network can change.

### Worked example: Arrange, Act, Assert
```python
def test_unscored_record_has_safe_fallback():
    # Arrange: make a tiny upstream record without metrics, matching
    # CVE-2026-90004 from the practice dataset, which really is unscored.
    upstream = {"cve": {"id": "CVE-2026-90004", "descriptions": [], "metrics": {}}}

    # Act: convert it using the normaliser.
    result = normalise_cve(upstream)

    # Assert: check the two important promises.
    assert result["score"] is None
    assert result["description"] == "No English description supplied."
```
`def` starts a function. Comments explain each stage. `assert` fails the test when its condition is false. The existing test suite follows the same idea using fixtures.

## Run and read tests
With your virtual environment active (`.venv\Scripts\Activate.ps1` on Windows, `source .venv/bin/activate` on macOS/Linux — see Lesson 4.4):
```bash
pytest -q
ruff check .
```
`-q` means quieter output. `ruff` checks style and likely mistakes. Read `tests/test_normalisers.py`, then identify Arrange, Act and Assert. Read `tests/test_cache.py`: `monkeypatch` temporarily replaces the network function so failure is safe and repeatable.

### Practise
1. Read `tests/test_normalisers.py` and label its Arrange, Act and Assert statements in your notebook or evidence record.
2. Run one file: `pytest -q tests/test_normalisers.py`.
3. Change one expected value in a temporary local copy, run the test, read the failure, then undo the change with `git restore tests/test_normalisers.py`. A red test contains useful information: expected value, actual value and line number.

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

# Lesson 12 — Deploy with Gunicorn, systemd and Nginx
**Effort:** substantial. **Suggested Git checkpoint:** `deploy vulnerability dashboard securely`; **release tag:** `v1.0.0`.

Follow `deployment/DEPLOYMENT.md` in order. It is written so you can verify each step yourself. This workbook explains the why; that guide gives exact verified commands and rollback. Every command in this lesson is typed into **LISH**, not SSH — reopen it from the Linode Cloud Manager exactly as you did in Lesson 2. Do not skip the firewall checks; you no longer need the "keep a second SSH session open" precaution from a normal deployment, because LISH cannot be locked out by a firewall or SSH mistake, but you should still verify before moving on out of good habit.

## Production terms
* **Gunicorn:** production server that runs Flask worker processes; bind it to `127.0.0.1:8000`, not the public internet.
* **systemd:** Ubuntu service manager. It starts Gunicorn after reboot and keeps logs.
* **Nginx:** public reverse proxy. It receives web traffic, serves as a controlled front door and forwards to Gunicorn.
* **UFW:** host firewall, enforced inside the server. Allow SSH and Nginx HTTP/HTTPS only.
* **Linode Cloud Firewall:** a second, independent firewall enforced by Linode at the network edge, before traffic reaches the server at all (set up in Lesson 3). Both this and UFW must agree before a port is reachable.
* **HTTPS:** encryption between browser and Nginx. A public trusted certificate needs a valid domain pointing at the server; a bare private IP normally cannot receive one.

## Deployment checklist
1. Open LISH and create the `vulnerability-dashboard` non-root service user and `/srv/vulnerability-dashboard` directory with correct ownership, exactly as in Lesson 3.
2. Install `git`, `python3-venv`, `python3-pip` and `nginx` with `apt`, then clone **your own public repository** straight onto the server:
   ```bash
   sudo git clone https://github.com/YOUR-GITHUB-USERNAME/vulnerability-dashboard.git /srv/vulnerability-dashboard
   ```
   Because the repository is **public**, this needs no SSH key, no deploy key and no GitHub sign-in at all — anyone, including this server, can read a public repository over plain HTTPS. This is one of the real advantages of the public-repo workflow: the server-side clone is the simplest part of the whole deployment.
3. Create `/srv/vulnerability-dashboard/.venv` (a second, independent virtual environment from the one on your laptop — see Lesson 4.4) and install the **pinned production** requirements (`requirements.txt`, not `requirements-dev.txt`; the server does not need `pytest`/`ruff`).
4. Put secrets only in `/etc/vulnerability-dashboard/vulnerability-dashboard.env`, owned root and readable by the service group; never in Git. **Because LISH has no file upload or paste-from-clipboard-into-a-file mechanism beyond your browser's normal copy/paste, you will type or paste this file's contents directly into `nano` inside the console** — there is no other route for a secret to reach this server. This is a second, physical reason (on top of the "public repository" reason from Lesson 4) that secrets can never travel through Git: they simply have no path there.
5. Test Gunicorn manually from a second LISH tab/window with `curl http://127.0.0.1:8000/health`.
6. Copy the provided systemd service, run `daemon-reload`, enable/start, inspect `systemctl status` and `journalctl -u vulnerability-dashboard`.
7. Copy Nginx configuration, set the real domain (or `_` for a temporary IP-only test), run `sudo nginx -t` **before** reload, then reload and test public routes/static CSS.
8. Apply the UFW Nginx rule. Check `ss -tulpn`. Then, in the Linode Cloud Manager, confirm your Cloud Firewall (Lesson 3) allows inbound 80/443 and does **not** allow inbound 22 from the public internet — you have no legitimate use for it, since you only ever connect via LISH.
9. If a domain exists, point its DNS at your Linode's public IP address, then obtain/test Certbot HTTPS; otherwise document the HTTP/private-classroom limitation.
10. Reboot only after recording a working rollback path and prove the service returns after reboot.
11. Tag the tested, working deployment on your laptop, and push the tag: `git tag -a v1.0.0 -m "First classroom release"` then `git push --tags`.

## Updating the live site: the day-2 workflow
Everything above gets the dashboard running for the first time. From now on, every future change follows the same short loop, and it is worth memorising the shape of it, because this — not the one-off setup above — is what you will actually do most often:

```text
1. Edit code on your laptop, in VS Code
2. Test locally: pytest -q, then python app.py
3. git add / git commit / git push   (to your public GitHub repository)
4. Open LISH (Linode Cloud Manager → your Linode → Launch LISH Console)
5. cd /srv/vulnerability-dashboard && sudo -u vulnerability-dashboard git pull
6. sudo systemctl restart vulnerability-dashboard
7. curl -i http://127.0.0.1:8000/health, then check the public site
```

Notice what does **not** appear in that list: there is no direct copy from your laptop to the server at any point. Step 3 publishes your change to GitHub; step 5 is the server independently fetching it. If `git pull` reports a conflict on the server, something has changed the server's copy independently of GitHub (for example, a file was hand-edited directly in LISH) — resolve it the same way you learned in Lesson 4's merge-conflict exercise, or, for a production server, prefer to discard the local change (`git checkout -- <file>`) and keep your GitHub history as the single source of truth.

## Worked example: diagnosing a failed deploy
### Scenario
You run `systemctl status vulnerability-dashboard --no-pager` and see `Active: failed`. The public Nginx page displays `502 Bad Gateway`.

### Reasoning route
1. A 502 means Nginx could not get a suitable response from the upstream application. It does not automatically mean Nginx is broken.
2. In LISH, run `curl -i http://127.0.0.1:8000/health`. If it cannot connect, investigate Gunicorn/systemd first.
3. Run `journalctl -u vulnerability-dashboard -n 50 --no-pager`. Read the first relevant error line.
4. Suppose it says the Python executable does not exist. Compare `ExecStart` in `/etc/systemd/system/vulnerability-dashboard.service` with `ls -l /srv/vulnerability-dashboard/.venv/bin/gunicorn`.
5. Correct only the path, run `sudo systemctl daemon-reload`, then `sudo systemctl restart vulnerability-dashboard`.
6. Re-test local health, then `sudo nginx -t`, then the public page. Record the evidence.

Do not restart every service repeatedly without reading logs. The order above identifies which layer failed and proves the repair. Use `TROUBLESHOOTING.md` for further decision trees (site will not load, Nginx loads but the app does not, Gunicorn works manually but systemd fails, NVD errors, CSS/JS not loading, permission denied, can't push to GitHub).

---

# Lesson 13 — Present, evaluate and extend
**Effort:** medium. **Suggested Git checkpoint:** `document final evaluation`.

## Final demonstration checklist
Demonstrate: (1) dashboard, (2) OWASP content, (3) live/recent cached CVEs, (4) search/filter, (5) failure handling, (6) request architecture, (7) Git history, (8) tests, (9) security controls, (10) one design decision, (11) one diagnosed problem, (12) next feature.

### Likely questions and strong answers
* **Why cache?** "It makes pages faster and reduces NVD rate-limit pressure. If NVD fails, we label older data as stale rather than pretending it is fresh."
* **Why Nginx and Gunicorn?** "Nginx is the public reverse proxy. Gunicorn runs Flask privately on localhost. This avoids exposing the development server."
* **How did you handle untrusted descriptions?** "Jinja escapes template values and our JavaScript uses `textContent`, not `innerHTML`."
* **Why did the server not need an SSH key or a deploy token to get your code?** "The repository is public, so `git clone`/`git pull` over HTTPS needs no authentication at all — only pushing requires proving who you are, and that only ever happens from my laptop."
* **How does a change get from your laptop to the live site?** "I push it to my GitHub repository, then separately log into the server through LISH and run `git pull` there — the two machines never talk to each other directly."
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

1. **No CVSS score:** a card has no score. *Hints:* inspect `None`; use the existing fallback. *Success:* "Not scored" and no crash. *Practises:* optional data.
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
13. **No visible label:** a form input has no associated label. *Hints:* `<label for>` and matching `id`. *Success:* the field is identifiable without seeing the page. *Practises:* accessible forms.
14. **Comprehension confusion:** a list/generator expression is hard to read. *Hints:* rewrite it as a plain `for` loop first, then compare. *Success:* the same output either way, plus a plain-English explanation. *Practises:* Python fundamentals.

# Appendix B — Responsible AI assistance log

AI may explain errors, unfamiliar syntax, test ideas, a small function, fixtures, options and documentation. It must not write the assessed project without your understanding; receive secrets; authorise unexplained commands; replace testing; or be treated as certain security advice. Follow your provider/course disclosure rules.

|Date|Question asked|Tool|Useful response|What I verified|What I changed|What I learned|
|---|---|---|---|---|---|---|
| | | | | | | |
