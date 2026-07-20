# Changelog
This project uses semantic versioning: **major** changes may require migration, **minor** adds compatible features, **patch** fixes compatible bugs.

## [1.1.0] - 2026-07-20
- Restructured `STUDENT_GUIDE.md` into a single linear 13-lesson workbook: folded the former standalone appendices (foundation labs, design studio, web-page reading, worked examples) directly into the lessons that use them, added a reusable eight-record invented practice dataset, a Python-fundamentals lesson, and an expanded HTML/CSS/JavaScript foundations lesson with a from-scratch practice page.
- Added guided "build it yourself" tasks: authoring a brand-new Flask route/template and a brand-new JSON content file, verified end-to-end.
- Reformatted `templates/*.html`, `static/css/styles.css` and `static/js/dashboard.js` from single-line minified files into readable, indented source so the workbook's "read this file" exercises are actually followable; behaviour and test results unchanged.
- Updated `README.md` and `TEACHING_NOTES.md` to match the new lesson structure and challenge-card count.

## [1.0.0] - 2026-07-20
- Initial Vulnerability Dashboard reference Flask dashboard, OWASP teaching dataset, NVD/CISA clients, cache, filters, tests, security review and Ubuntu deployment pack.
