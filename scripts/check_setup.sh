#!/usr/bin/env bash
set -euo pipefail
command -v python3 >/dev/null
python3 -c 'import flask, requests; print("Python dependencies: OK")'
test -f data/owasp_top_10.json
echo "CyberScope setup checks: OK"
