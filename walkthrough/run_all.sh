#!/usr/bin/env bash
# Full clean capture + site build. ~20 minutes against bometfeedbackhub.digit.org.
set -euo pipefail
cd "$(dirname "$0")"
PY=.venv/bin/python

echo "== wiping previous capture (screenshots only; _recon is kept)"
rm -rf output/en

echo "== configurator (sign-in + management console)"
$PY capture_configurator.py

echo "== onboarding wizard (phases 1-4)"
$PY capture_onboarding.py

echo "== employee UI"
$PY capture_employee.py

echo "== rendering the site"
$PY build_site.py

echo
echo "Done. Serve it with:  cd output && python3 -m http.server 8080"
