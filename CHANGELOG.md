# Changelog
This project uses semantic versioning: **major** changes may require migration, **minor** adds compatible features, **patch** fixes compatible bugs.

## [1.2.0] - 2026-07-20
- Reworked the workbook and deployment docs for the real classroom workflow: development on the student's own laptop in VS Code, a **public** GitHub repository as the only bridge between machines, and a **Linode** server reached exclusively through the browser-based **LISH** console (SSH to the server is unavailable on the school network).
- Rewrote Lesson 2 around LISH login, root-password reset, and creating a personal sudo user (no SSH keys involved); rewrote Lesson 4 into a laptop setup lesson (VS Code/Python/Git install, GitHub account and public repo creation, HTTPS+sign-in authentication instead of SSH keys) ahead of the existing Python-fundamentals content; reframed Lesson 3's SSH/UFW hardening around LISH being an unlockable-out-of safety net, and added a Linode Cloud Firewall step that explicitly closes port 22 to the internet.
- Rewrote Lesson 12's deployment checklist for a public-repo `git clone`/`git pull` (no deploy keys or credentials needed on the server) and added an explicit "day-2" laptop → push → LISH → pull update loop, plus a note that server secrets must be typed by hand in `nano` since LISH has no file upload.
- Added Windows/macOS/Linux command variants where laptop-side steps genuinely differ (Python/Git install, venv activation, port/process inspection).
- Updated `deployment/DEPLOYMENT.md`, `TROUBLESHOOTING.md` (new LISH and GitHub-push-auth decision trees), `TEACHING_NOTES.md` and `README.md` to match.

## [1.1.0] - 2026-07-20
- Restructured `STUDENT_GUIDE.md` into a single linear 13-lesson workbook: folded the former standalone appendices (foundation labs, design studio, web-page reading, worked examples) directly into the lessons that use them, added a reusable eight-record invented practice dataset, a Python-fundamentals lesson, and an expanded HTML/CSS/JavaScript foundations lesson with a from-scratch practice page.
- Added guided "build it yourself" tasks: authoring a brand-new Flask route/template and a brand-new JSON content file, verified end-to-end.
- Reformatted `templates/*.html`, `static/css/styles.css` and `static/js/dashboard.js` from single-line minified files into readable, indented source so the workbook's "read this file" exercises are actually followable; behaviour and test results unchanged.
- Updated `README.md` and `TEACHING_NOTES.md` to match the new lesson structure and challenge-card count.

## [1.0.0] - 2026-07-20
- Initial Vulnerability Dashboard reference Flask dashboard, OWASP teaching dataset, NVD/CISA clients, cache, filters, tests, security review and Ubuntu deployment pack.
