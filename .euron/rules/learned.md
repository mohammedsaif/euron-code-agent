<!-- Written by Euron Code after each task. It is rewritten automatically: put your own rules in
     another file in .euron/rules/. -->

# Learned in this project

- Tests: `python -m pytest -q tests/test_api.py` works here (passed 2x, last 2026-11-18). Use it to verify changes.
- Tests: `cd C:\Users\Dell\euron-code-agent\calculator-euron && python -m pytest -q` works here (passed 1x, last 2026-11-18). Use it to verify changes.
- Tests: `cd calculator-euron && python -m pytest -q` has failed 2x and never passed; check why before relying on it.
- Tests: `python -m pytest -q calculator-euron/tests/test_api.py` has failed 3x and never passed; check why before relying on it.

## Security (from .euron/security/assessment.md)
- This code base has had: html inserted without escaping (xss) (SEC050). Render text, or sanitise the HTML (DOMPurify / bleach) before inserting it. Do not add more; fix the existing ones when you touch those files.
