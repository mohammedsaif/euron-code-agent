"""FastAPI application for the Calculator API.

Endpoints:
  GET  /health           – health check
  POST /add              – addition
  POST /subtract         – subtraction
  POST /multiply         – multiplication
  POST /divide           – division
  POST /power            – exponentiation
  POST /calculate        – safe expression evaluation
  GET  /history          – last 20 calculations
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path

from . import history as calc_history
from .models import (
    CalculateRequest,
    CalculateResponse,
    HistoryEntry,
    MathResponse,
    OperandsRequest,
)
from .parser import safe_eval

app = FastAPI(title="Calculator API", version="1.0.0")

# Serve the calculator UI
@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

@app.get("/health")
def health_check() -> dict:
    """Return a simple status check."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Binary math helpers
# ---------------------------------------------------------------------------

def _clean_result(value: int | float) -> int | float:
    """Round float results to 10 decimal places to avoid floating-point artefacts.

    e.g. 0.1 + 0.2 = 0.30000000000000004  →  0.3
    """
    if isinstance(value, float):
        return round(value, 10)
    return value


def _do_binary(
    operation: str,
    req: OperandsRequest,
    fn,
) -> MathResponse:
    """Execute a binary math operation and record it in history."""
    input_str = f"{req.a} {operation_symbol(operation)} {req.b}"
    try:
        result = fn(req.a, req.b)
    except ZeroDivisionError:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    except OverflowError:
        raise HTTPException(status_code=400, detail="Power operation overflow")

    if operation == "power" and abs(req.b) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Exponent absolute value must not exceed 1000",
        )

    result = _clean_result(result)
    calc_history.record(operation, input_str, result)
    return MathResponse(operation=operation, a=req.a, b=req.b, result=result)


def operation_symbol(op: str) -> str:
    """Map an operation name to its symbol."""
    symbols = {
        "add": "+",
        "subtract": "-",
        "multiply": "*",
        "divide": "/",
        "power": "**",
    }
    return symbols.get(op, op)


@app.post("/add")
def add(req: OperandsRequest) -> MathResponse:
    """Add two numbers."""
    return _do_binary("add", req, lambda a, b: a + b)


@app.post("/subtract")
def subtract(req: OperandsRequest) -> MathResponse:
    """Subtract b from a."""
    return _do_binary("subtract", req, lambda a, b: a - b)


@app.post("/multiply")
def multiply(req: OperandsRequest) -> MathResponse:
    """Multiply two numbers."""
    return _do_binary("multiply", req, lambda a, b: a * b)


@app.post("/divide")
def divide(req: OperandsRequest) -> MathResponse:
    """Divide a by b."""
    if req.b == 0:
        raise HTTPException(status_code=400, detail="Division by zero is not allowed")
    return _do_binary("divide", req, lambda a, b: a / b)


@app.post("/power")
def power(req: OperandsRequest) -> MathResponse:
    """Raise a to the power of b."""
    if abs(req.b) > 1000:
        raise HTTPException(
            status_code=400,
            detail="Exponent absolute value must not exceed 1000",
        )
    return _do_binary("power", req, lambda a, b: a ** b)


# ---------------------------------------------------------------------------
# Expression calculator
# ---------------------------------------------------------------------------

@app.post("/calculate")
def calculate(req: CalculateRequest) -> CalculateResponse:
    """Evaluate a mathematical expression safely using an AST parser."""
    expr = req.expression.strip()
    if not expr:
        raise HTTPException(status_code=400, detail="Expression must not be empty")

    try:
        result = safe_eval(expr)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from None

    calc_history.record("calculate", expr, result)
    return CalculateResponse(expression=expr, result=result)


# ---------------------------------------------------------------------------
# History
# ---------------------------------------------------------------------------

@app.get("/history")
def get_history() -> list[HistoryEntry]:
    """Return the last 20 calculations, newest first."""
    return calc_history.get_history()
