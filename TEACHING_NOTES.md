# Vulnerability Dashboard delivery guide

## Purpose and preparation
This is a one-week, progressive project for Digital T Level learners working through a new applied project. The goal is independent explanation and evidence, not a perfect copied dashboard. Before the first lesson, prepare a supported Ubuntu LTS cloud instance per individual/team; a named student account with SSH public key; provider-console recovery/snapshot access; a private repository or local Git option; and a safe method for recording evidence. Confirm your institution's safeguarding, acceptable use and AI-disclosure policies.

Verify the current official OWASP Top 10 edition, NVD API 2.0 documentation, and CISA KEV JSON URL **before** delivery. The prior build environment could not reach them. Record the date and update/review `data/owasp_top_10.json` if required. Do not present the included edition as current until this check is complete.

## Learning outcomes
Students should be able to: explain public/private IP, SSH keys, users and sudo; navigate Linux and interpret a command before running it; make meaningful Git commits; create semantic responsive pages; trace a request through Flask/templates; explain JSON/API/status/timeout; normalise optional data; justify caching; make a keyboard-safe interface; write/read tests; diagnose with DevTools/logs/curl; identify security controls/residual risks; deploy least-privilege Gunicorn behind Nginx; and explain decisions to a non-technical audience.

## Suggested delivery sequence

|Lesson|Delivery demonstration|Minimum student evidence|Intervene when|
|---|---|---|---|
|1: problem|Score vs KEV/context scenario|audience, sketch, decision|student treats CVSS as risk|
|2: Ubuntu|SSH host key, `pwd`/`cd`/`ls`, log command|navigation challenge|student uses destructive command blindly|
|3: hardening|second SSH session, `ss`, UFW numbered rules|change/verify/undo record|SSH/firewall change lacks rollback|
|4: tools/Git|venv activation, one atomic commit/diff|history and ignored `.env`|student adds secret or works as root|
|5: Flask|one route/template/DevTools inspection|edited sentence and health curl|debug server exposed publicly|
|6: OWASP|JSON object/list, official vs teaching text|valid JSON and reviewed wording|student changes categories without source|
|7: API|`curl -i`, fixture nesting, 429 response|identify fields/status|live calls are repeated|
|8: cache|fresh/stale cache and mock failure|request-flow explanation|student assumes cache is always current|
|9: UX|keyboard and narrow view|filter/empty-state evidence|colour-only or `innerHTML` change|
|10: test/security|AAA test and header curl|passing test/security worksheet|test calls public API|
|11: deploy|manual Gunicorn → systemd → Nginx|health/log/service output|root service or public Gunicorn|
|12: demo|model evidence-led explanation|individual demonstration|student cannot explain own code|

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
For learners needing support: work offline from fixtures, use a command card, pair on one function, give a diagram with blank labels, and accept annotated screenshots plus oral explanation. For faster learners: choose an extension, write a failing test first, conduct a peer accessibility/security review, or add CI. Review commits after Lessons 4, 6, 8, 10 and 11. Check readable names, small changes, no secrets, tests, safe external text, decision evidence and each student's individual contribution to code/test/docs/deployment.

## Assessment and final demonstration
Use [ASSESSMENT_RUBRIC.md](ASSESSMENT_RUBRIC.md) with evidence, not impressions. Give each student 5–8 minutes: demonstrate dashboard/OWASP/CVEs/filter/failure; trace Browser→Nginx→Gunicorn→Flask→cache/API; show a commit/test/log; explain a security control, design choice, real diagnosis and next step. Ask follow-ups from Lesson 12. A polished page without understanding does not demonstrate secure achievement.

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
|Extra port|Use `ufw status numbered`, delete exact rule, preserve OpenSSH.|
|systemd|Read journal; correct user/path/environment/ownership, then daemon-reload.|
|Mobile|Use responsive view; correct media/layout rather than hiding controls.|
|No matches|Show count/empty state and clear action.|
|OWASP update|Verify official release, update local reviewed JSON, validate/test/commit.|
|Dependency|Confirm installed version/advisory scope; patch in branch; test/document decision.|
|Priority|CVSS=technical severity; KEV=known exploitation; assets/exposure/fix context decide action.|
