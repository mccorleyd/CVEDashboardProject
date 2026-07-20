# Mentor guide
## Outcomes and sequence
Students explain Linux access/least privilege, use Git evidence, create accessible HTML/CSS, trace Flask routes, retrieve/normalise/cache API data, test failures, assess security, and deploy. Deliver the ten Student Guide phases in order; demonstrate a **small** example, then remove support. Prepare a Ubuntu LTS instance with a named student, SSH keys, a backup/snapshot and provider firewall restricted to the classroom IP where possible.

## Demonstrate and coach
Show terminal navigation, one commit, a route/template, one JSON path, one normaliser test, DevTools Network, stale cache, then systemd/Nginx. Likely blocks: virtualenv activation, indentation, JSON commas, dates, permissions, service working directory and confusing CVSS with risk. Ask: “What status code/log proves that?”, “What is the smallest input?”, “Where is this value transformed?”, “What would a safe failure look like?” Do not immediately provide a patch.

## Differentiation/review
Slower: use fixture/cache first, pair-program one function, sentence starters and checked command cards. Faster: choose extensions, peer accessibility audit, add mocks/CI. Review at commits 3, 5, 7, 9 and pre-deploy: no secrets; input/output handling; test evidence; readable names; decision record. Responsible AI is a teaching aid, not an author: require an AI log, explanation, independent test and course-policy disclosure.

## Challenge cards — student-facing
1 **No score:** a CVE lacks CVSS. Hint: compare `None`; success: “Not scored”, no crash; concepts optional fields. 2 **429:** NVD limits requests. Hint: cache/status; success: friendly warning; rate limits. 3 **Timeout:** request stalls. Hint: timeout/fixture; success: stale fallback; resilience. 4 **Odd description:** external text contains markup. Hint: text node; success: displayed literally; output encoding. 5 **Stale cache:** TTL expires. Hint: timestamp; success: visible warning; caching. 6 **Extra port:** port opened accidentally. Hint: `ufw status`; success: remove rule; least exposure. 7 **systemd failure:** manual Gunicorn works. Hint: `journalctl`; success: correct user/path; service context. 8 **Mobile CSS:** narrow screen broken. Hint: responsive mode; success: readable nav; responsive design. 9 **No matches:** filters combine. Hint: clear; success: empty message; UX. 10 **New OWASP:** release changes. Hint: local JSON process; success: reviewed update; maintenance. 11 **Vulnerable dependency:** advisory appears. Hint: pin/test; success: documented update/decision; supply chain. 12 **Explain priorities:** manager asks score vs KEV. Hint: evidence/context; success: plain answer; risk communication.

## Mentor-only solution prompts
1 use `score is None`; 2 do not retry repeatedly—show cache; 3 mock `NvdError`; 4 retain `textContent`/Jinja escaping; 5 set low TTL then offline; 6 `sudo ufw delete allow PORT`; 7 inspect unit `WorkingDirectory`, paths and ownership; 8 use 650px media query; 9 prove reset returns results; 10 verify OWASP first, then update/test/commit; 11 check advisory against installed version and update in a branch; 12 CVSS=technical severity, KEV=known exploitation, neither replaces asset context.

## Final format
Each student gets 5–8 minutes plus questions. Ask: Why cache? Why non-root? How did you test failure? What does Nginx do? Strong evidence is a command output, test, log and plain-English explanation—not just a polished screen.
