# Vulnerability Dashboard delivery guide

## Purpose and preparation
This is a one-week, progressive project for Digital T Level learners working through a new applied project. The goal is independent explanation and evidence, not a perfect copied dashboard.

**Workflow assumed by this version of the workbook:** students develop locally on their own laptop in VS Code, push to their own **public** GitHub repository, and separately log into a **Linode** cloud server through its browser-based **LISH console** to deploy — SSH to the server is assumed blocked by the institution's network, so LISH (not SSH) is the only access route taught. Before the first lesson, prepare: a Linode instance per student/team, with its root password recorded (or resettable from the Cloud Manager); confirmation that students can reach `cloud.linode.com` and `github.com` from the school network; each student able to create their own GitHub account and a public repository (either from a provided template or from scratch); VS Code installable on student laptops (or already imaged); Linode account/provider-console recovery access for staff; and a safe method for recording evidence. Confirm your institution's safeguarding, acceptable use and AI-disclosure policies, and specifically confirm your policy on students publishing coursework to public repositories before Lesson 4.

Verify the current official OWASP Top 10 edition, NVD API 2.0 documentation, and CISA KEV JSON URL **before** delivery. The prior build environment could not reach them. Record the date and update/review `data/owasp_top_10.json` if required. Do not present the included edition as current until this check is complete.

## Learning outcomes
Students should be able to: explain public/private IP, users and sudo, and why this project reaches its server through LISH rather than SSH; navigate Linux and interpret a command before running it; write core Python (variables, lists, dicts, loops, functions, comprehensions); author semantic, responsive HTML/CSS/JavaScript from a blank file, not only edit existing pages; set up a local Python/Git/VS Code environment and authenticate to GitHub without SSH keys; make meaningful Git commits to a public repository and understand what "public" really means; trace a request through Flask/templates; explain JSON/API/status/timeout; normalise optional data; justify caching; make a keyboard-safe interface; write/read tests; diagnose with DevTools/logs/curl; identify security controls/residual risks; deploy least-privilege Gunicorn behind Nginx on a server they never SSH into; explain the laptop → GitHub → server update loop; and explain decisions to a non-technical audience.

## Suggested delivery sequence

The workbook is a single linear read: each lesson now contains the worked examples and foundation labs it needs, rather than pointing out to separate appendices. Section 0 introduces a reusable eight-record invented CVE dataset that recurs from Lesson 1 through Lesson 11 — use it to check a student's predictions against real output without waiting on live data. Lessons 5 onward (HTML/CSS/JS, Flask, OWASP JSON, APIs, normalisation, UX, testing) happen on the student's own laptop; only Lessons 2, 3 and 12 happen on the Linode server via LISH.

|Lesson|Delivery demonstration|Minimum student evidence|Intervene when|
|---|---|---|---|
|1: problem|Score vs KEV/context scenario (3 invented records)|audience, sketch, decision, priority order|student treats CVSS as risk|
|2: Linux foundations|Open LISH from the Cloud Manager, create a personal sudo user, paths/files/permissions/help labs|navigation challenge, permissions checkpoint, own-user login proof|student stays logged in as root, or uses a destructive command blindly|
|3: hardening|Linode Cloud Firewall + UFW both configured, port 22 closed externally|change/verify/undo record, firewall rule screenshot|firewall change lacks rollback, or port 22 left open with no justification|
|4: laptop/Python/Git|VS Code + Python + Git installed, GitHub account/public repo created, comprehension built from a loop, one atomic commit/push|`count_exploited` function, pushed history, ignored `.env`|student adds a secret, commits to the wrong (private/class) repo, or cannot explain `.get()`|
|5: HTML/CSS/JS foundations|standalone practice page built locally: semantic HTML, custom-property CSS, a JS toggle with `textContent`|rendered practice page, keyboard test, contrast evidence|colour-only signal, hidden focus outline, or `innerHTML` used|
|6: Flask|one **new** route+template built from nothing on the laptop, plus DevTools inspection|`/practice` page working, health curl|debug server exposed publicly|
|7: OWASP|JSON object/list, a from-scratch practice JSON file, official vs teaching text|valid practice JSON and reviewed real-file wording|student changes categories without source|
|8: API|`curl -i`, fixture nesting, 429 response|identify fields/status|live calls are repeated|
|9: cache|fresh/stale cache and mock failure|request-flow explanation|student assumes cache is always current|
|10: UX|keyboard and narrow view, filter predictions checked against the dataset|filter/empty-state evidence|colour-only or `innerHTML` change|
|11: test/security|AAA test and header curl|passing test/security worksheet|test calls public API|
|12: deploy|LISH console, public-repo clone with no credentials, manual Gunicorn → systemd → Nginx, 502 diagnosis walkthrough, a completed laptop→push→LISH→pull update cycle|health/log/service output, correct `v1.0.0` tag, evidence of one full update-loop cycle|root service, public Gunicorn, or a student attempting to SSH/scp into the server|
|13: demo|model evidence-led explanation|individual demonstration|student cannot explain own code|

## Coaching approach
Use a gradual-release routine: **I do** one small example; **we do** one modification; **you do** a related task with a checkpoint. Ask questions before giving code: “What is your current folder?”, “What did the status code say?”, “What changed in `git diff`?”, “Which layer owns this error?”, “What can we test without the internet?”, “How will you undo that command?” Require students to read the error aloud and state a hypothesis.

### Common sticking points and productive prompts
* **Terminal anxiety:** ask them to run `pwd`, then `ls`, then state the target path before `cd`.
* **Virtual environment:** “Does the prompt show `(.venv)`? Which `python` is being used: `which python`?”
* **JSON syntax:** use `python -m json.tool`; ask which line/character the error names.
* **Indentation:** ask them to identify which block owns a line; use editor whitespace display.
* **API failures:** distinguish their code, network and upstream 429/500. Do not make more requests to “see if it changes”.
* **Permissions:** ask who owns the file and which user runs the service; use `ls -l`, not immediate `chmod 777`.
* **systemd:** compare shell environment with unit `User`, `WorkingDirectory`, `EnvironmentFile` and `ExecStart`; read journal first.

## Differentiation and review points
For learners needing support: work offline from fixtures, use a command card, pair on one function, give a diagram with blank labels, and accept annotated screenshots plus oral explanation. For faster learners: choose an extension, write a failing test first, conduct a peer accessibility/security review, or add CI. Review commits after Lessons 4, 7, 9, 11 and 12. Check readable names, small changes, no secrets, tests, safe external text, decision evidence and each student's individual contribution to code/test/docs/deployment.

## Assessment and final demonstration
Use [ASSESSMENT_RUBRIC.md](ASSESSMENT_RUBRIC.md) with evidence, not impressions. Give each student 5–8 minutes: demonstrate dashboard/OWASP/CVEs/filter/failure; trace Browser→Nginx→Gunicorn→Flask→cache/API; show a commit/test/log; explain a security control, design choice, real diagnosis and next step. Ask follow-ups from Lesson 13. A polished page without understanding does not demonstrate secure achievement.

## Responsible AI
Allow AI for explanations, small-code review, test ideas, fixture ideas and documentation only when students record it. Do not let AI receive secrets or replace evidence. Require the workbook AI log, a student explanation of every adopted line/command, and independent test/official-source verification. For security claims, model “AI output is a hypothesis, not authority.”

## Challenge cards and delivery-only answers
The student-facing cards are in Appendix A of the workbook. Do not show this section until an attempt is recorded.

|Card|Delivery-only answer direction|
|---|---|
|No score|Use `score is None`; retain “Not scored”.|
|429|Do not retry in a tight loop; use cache and friendly warning.|
|Timeout|Mock `NvdError`; confirm stale fallback.|
|Special characters|Keep Jinja escaping and `textContent`; never change to `innerHTML`.|
|Stale cache|Lower TTL temporarily; prove warning/restore default.|
|Extra port|Use `ufw status numbered`, delete exact rule; check the Linode Cloud Firewall too, since both layers must be correct.|
|systemd|Read journal; correct user/path/environment/ownership, then daemon-reload.|
|Mobile|Use responsive view; correct media/layout rather than hiding controls.|
|No matches|Show count/empty state and clear action.|
|OWASP update|Verify official release, update local reviewed JSON, validate/test/commit.|
|Dependency|Confirm installed version/advisory scope; patch in branch; test/document decision.|
|Priority|CVSS=technical severity; KEV=known exploitation; assets/exposure/fix context decide action.|
|No label|Check `<label for>` matches the input `id`; do not rely on placeholder text alone.|
|Comprehension confusion|Have the student rewrite it as a plain `for` loop first, confirm matching output, then explain the compact form.|
