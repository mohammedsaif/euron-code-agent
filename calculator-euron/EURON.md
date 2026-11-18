# calculator-euron

<!-- Written by Euron Code project setup. Run /init to let the model fill in the details. -->

Stack: Python, FastAPI, Docker, Docker Compose

## Commands
- `pip install -r requirements.txt`
- `python -m pytest`

## Layout
```
app/  (6 files)
  __init__.py
  history.py
  main.py
  models.py
  parser.py
  static/
tests/  (2 files)
docker-compose.yml
Dockerfile
README.md
requirements-dev.txt
requirements.txt
```

Entry points: app/main.py

## Conventions
- (add the conventions of this project here)
- ## Prompt 5: Repo hygiene + README + prompt log
```
Prepare the repo for a public GitHub submission.

1. .gitignore: Python, venv, .env, __pycache__, .pytest_cache, .DS_Store. Do NOT ignore the .euron folder.
2. .env.example with APP_PORT=8000 (no real secrets), and make the app read the port only where it's needed.
3. prompts.md: list every prompt I gave you in this session, in order, each with one line on what it produced.
   Include the vague prompt "make a calculator api" from my scratch test as Prompt 0.
4. README.md with these sections:
   - Project overview
   - Tech stack
   - Project structure (tree)
   - Run locally (venv, pip install -r requirements-dev.txt, uvicorn, pytest)
   - Run with Docker (build, run, docker-compose up)
   - API endpoints table with an example request/response for each
   - Screenshots (placeholders: screenshots/docs.png, screenshots/app.png, screenshots/tests.png)
   - "Working with Euron Code" containing:
       * Vague vs precise prompt: <leave placeholder for me to fill>
       * What I fixed after reviewing the agent's code: <placeholder>
       * Allowance used (/usage before vs after): <placeholder>
       * Docker image size: <placeholder>
Do not invent the placeholder content; I will write it.
```

Then:
```
/usage          ← screenshot (allowance AFTER)
```

---

## D. README text to fill in yourself (templates)

**Vague vs precise:**
> The vague prompt "make a calculator api" gave me a single file that used eval(), with no validation, tests or history. The precise prompt listed the file structure, endpoints, error codes and test cases, so the agent produced a modular app with a safe AST parser and N passing tests on the first try. Being specific about constraints (no eval, 400 on divide by zero) mattered most.

**What I fixed:**
> /exit
