# euron-code-agent

Euron Code workspace. No application code yet.

Stack: none

## Commands
- (none — no project scaffolding or manifest yet)

## Layout
```
.euron/          Euron Code config (rules, commands, settings)
EURON.md         this file
```

## Conventions
- Keep EURON.md under 70 lines.
- Security rules (.euron/rules/security.md): no secrets in code, parameterised SQL, sanitise HTML.
- Testing rules (.euron/rules/testing.md): tests must be deterministic; run after every change.
- Git rules (.euron/rules/git.md): never commit/push/rebase without explicit ask.

## Repo map
```
.euron/
  settings.json
  rules/git.md, security.md, testing.md, learned.md
  commands/commit.md, fix-tests.md, pr.md, security-review.md
EURON.md
.gitignore
```
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
> The agent's parser let nested powers like `2**2**2**2**2` run without limit, which could hang the server. I added an exponent cap and an AST depth limit inside the parser, plus a test. I also added a fixture that clears history between tests.

**Usage:** `Before: X · After: Y · Task used about Z% of my allowance.`
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
> The agent's parser let nested powers like `2**2**2**2**2` run without limit, which could hang the server. I added an exponent cap and an AST depth limit inside the parser, plus a test. I also added a fixture that clears history between tests.

**Usage:** `Before: X · After: Y · Task used about Z% of my allowance.`
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
> The agent's parser let nested powers like `2**2**2**2**2` run without limit, which could hang the server. I added an exponent cap and an AST depth limit inside the parser, plus a test. I also added a fixture that clears history between tests.

**Usage:** `Before: X · After: Y · Task used about Z% of my allowance.`
