# Calculator API

A production-quality FastAPI calculator with safe expression parsing, operation history, and Docker support.

## Setup

```bash
# install runtime + dev dependencies (pytest, httpx)
pip install -r requirements-dev.txt

# run tests
pytest -q
```

`requirements.txt` has only the runtime packages. `requirements-dev.txt`
adds `pytest` and `httpx` on top.

## Run locally

```bash
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API docs.

## Run with Docker

```bash
docker build -t calculator-api .
docker run -p 8000:8000 calculator-api
```

Or with Docker Compose:

```bash
docker compose up --build
```

## API Endpoints

| Method | Path         | Description                     |
| ------ | ------------ | ------------------------------- |
| GET    | /health      | Health check                    |
| POST   | /add         | Add two numbers                 |
| POST   | /subtract    | Subtract b from a               |
| POST   | /multiply    | Multiply two numbers            |
| POST   | /divide      | Divide a by b                   |
| POST   | /power       | Raise a to the power of b       |
| POST   | /calculate   | Evaluate a math expression      |
| GET    | /history     | Last 20 calculations            |

All `/add` through `/power` endpoints accept `{"a": <number>, "b": <number>}`.
The `/calculate` endpoint accepts `{"expression": "<math string>"}`.

## Validation

- `a` and `b` must be numbers (int or float); strings return 422.
- Divide by zero returns 400.
- Exponent `|b| > 1000` on `/power` returns 400.
- Empty or >200 character expressions on `/calculate` return 400.
- No `eval()` or `exec()` — expressions are parsed safely via Python's `ast` module.
