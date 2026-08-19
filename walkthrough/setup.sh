#!/usr/bin/env bash
# One-time setup: python env + the scraper library + a headless chromium.
set -euo pipefail
cd "$(dirname "$0")"

python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m playwright install chromium

echo
echo "Ready. Capture everything with:  ./run_all.sh"
