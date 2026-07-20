# Vulnerability Dashboard assessment rubric

Assess evidence from the student's commits, decision record, terminal/log screenshots, tests, completed self-review, documentation and individual demonstration. A learner can be stronger in one row than another. “Secure” is the expected complete core standard; “Advanced” adds justified, tested independence.

|Area|Emerging|Developing|Secure|Advanced|
|---|---|---|---|---|
|Linux and server skills|Runs provided commands with continuous support.|Navigates folders and explains `pwd`, `ls`, `cd`, user and sudo.|Uses commands deliberately; records verify/undo; checks processes/ports/logs; never works as root unnecessarily; preserves LISH access to the server.|Diagnoses an unfamiliar service/permission issue methodically and explains least privilege.|
|Git and GitHub usage|Has an incomplete or single commit.|Uses status/add/commit with some messages.|Has logical commits, diff/history evidence, branch/merge or revert, tag, a working public repository, and no secrets ever pushed.|Resolves controlled conflict and uses history to support a safe rollback.|
|HTML and CSS|Edits static supplied content.|Uses headings/links/labels and basic styling.|Produces semantic, responsive layout with visible focus, non-colour severity text and contrast evidence.|Uses an accessibility audit to improve a real issue and explains trade-offs.|
|Python and Flask|Changes starter code without explanation.|Explains route/template relationship.|Explains request flow, configuration, routes, error page and readable functions.|Makes a small well-tested improvement without unnecessary abstraction.|
|API integration|Can name an API.|Uses fixture or manual request.|Explains GET/parameters/headers/status/JSON/timeouts and optional key handling.|Adds bounded, validated API functionality and explains rate-limit impact.|
|Data handling|Displays values directly.|Finds fields in fixture.|Normalises optional NVD fields; distinguishes CVE/CWE/CVSS/KEV; labels stale data.|Justifies prioritisation using assets/exposure/evidence rather than scores alone.|
|Error handling|Shows traceback or stops at error.|Reports one friendly error.|Uses timeout, explicit exceptions, cache fallback and safe missing-field display.|Adds meaningful failure test and a useful diagnosis guide.|
|Testing|Can run tests.|Explains one assertion.|Uses fixtures/mocks; unit/route/cache tests pass without live NVD.|Writes an independent valuable test or CI workflow.|
|Security|Can name a generic risk.|Keeps `.env` out of an obvious commit.|Completes review: headers, validation, output encoding, key handling, non-root, UFW/Linode Cloud Firewall evidence with port 22 closed externally.|Explains residual risks and improves one control with a test/review.|
|Deployment|Runs locally only.|Runs Gunicorn manually.|Nginx proxies to systemd-managed non-root Gunicorn; health/log/UFW verification recorded; code reached the server only via public-repo `git pull` through LISH.|Performs a tested update/rollback via the laptop→push→LISH→pull loop and documents HTTPS/DNS or limitation.|
|Documentation|Notes are missing or copied.|Some setup notes exist.|Clear decision, test, troubleshooting and source/limitation records.|Produces a concise guide understandable by a non-technical stakeholder.|
|Problem solving and communication|Cannot explain choices.|Answers direct prompts.|Explains one diagnosis, architecture, data limits and design choice in own words.|Adapts explanation for technical/non-technical audience and defends evidence-based trade-offs.|
