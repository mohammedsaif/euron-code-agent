"""Tests for the Calculator API.

Covers every endpoint plus edge cases: divide by zero, non-numeric input,
eval-injection attempts, operator precedence, parentheses, unary minus,
and history limit of 20.
"""

from fastapi.testclient import TestClient

from app.main import app
from app import history as calc_history

client = TestClient(app)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def setup_function() -> None:
    """Clear the shared history before every test."""
    calc_history.clear()


def _reset_history() -> None:
    """Clear the shared history before a test."""
    calc_history.clear()


# ---------------------------------------------------------------------------
# /health
# ---------------------------------------------------------------------------

def test_health() -> None:
    """GET /health returns 200 with status ok."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# Binary math endpoints
# ---------------------------------------------------------------------------

def test_add() -> None:
    """POST /add returns correct sum."""
    resp = client.post("/add", json={"a": 2, "b": 3})
    assert resp.status_code == 200
    data = resp.json()
    assert data["operation"] == "add"
    assert data["result"] == 5


def test_subtract() -> None:
    """POST /subtract returns correct difference."""
    resp = client.post("/subtract", json={"a": 10, "b": 4})
    assert resp.status_code == 200
    assert resp.json()["result"] == 6


def test_multiply() -> None:
    """POST /multiply returns correct product."""
    resp = client.post("/multiply", json={"a": 3, "b": 7})
    assert resp.status_code == 200
    assert resp.json()["result"] == 21


def test_divide() -> None:
    """POST /divide returns correct quotient."""
    resp = client.post("/divide", json={"a": 15, "b": 3})
    assert resp.status_code == 200
    assert resp.json()["result"] == 5


def test_divide_by_zero() -> None:
    """POST /divide with b=0 returns 400."""
    resp = client.post("/divide", json={"a": 10, "b": 0})
    assert resp.status_code == 400
    assert "Division by zero" in resp.json()["detail"]


def test_power() -> None:
    """POST /power returns correct result."""
    resp = client.post("/power", json={"a": 2, "b": 10})
    assert resp.status_code == 200
    assert resp.json()["result"] == 1024


def test_power_exponent_too_large() -> None:
    """POST /power with |exponent| > 1000 returns 400."""
    resp = client.post("/power", json={"a": 2, "b": 1001})
    assert resp.status_code == 400
    assert "1000" in resp.json()["detail"]


def test_power_negative_exponent_too_large() -> None:
    """POST /power with |exponent| > 1000 (negative) returns 400."""
    resp = client.post("/power", json={"a": 2, "b": -1001})
    assert resp.status_code == 400


def test_non_numeric_input() -> None:
    """POST /add with a string value returns 422."""
    resp = client.post("/add", json={"a": "abc", "b": 3})
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# /calculate
# ---------------------------------------------------------------------------

def test_calculate_simple() -> None:
    """POST /calculate with a simple addition."""
    resp = client.post("/calculate", json={"expression": "2 + 3"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 5


def test_calculate_precedence() -> None:
    """2 + 3 * 4 must follow operator precedence (14, not 20)."""
    resp = client.post("/calculate", json={"expression": "2 + 3 * 4"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 14


def test_calculate_parentheses() -> None:
    """(2 + 3) * 4 must be 20."""
    resp = client.post("/calculate", json={"expression": "(2 + 3) * 4"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 20


def test_calculate_unary_minus() -> None:
    """Unary minus: -3 + 2 must be -1."""
    resp = client.post("/calculate", json={"expression": "-3 + 2"})
    assert resp.status_code == 200
    assert resp.json()["result"] == -1


def test_calculate_division_by_zero() -> None:
    """Division by zero in expression returns 400."""
    resp = client.post("/calculate", json={"expression": "5 / 0"})
    assert resp.status_code == 400
    assert "Division by zero" in resp.json()["detail"]


def test_calculate_empty_expression() -> None:
    """Empty expression string returns 422 (min_length validation)."""
    resp = client.post("/calculate", json={"expression": ""})
    assert resp.status_code == 422


def test_calculate_whitespace_only() -> None:
    """Whitespace-only expression returns 400."""
    resp = client.post("/calculate", json={"expression": "   "})
    assert resp.status_code == 400
    assert "empty" in resp.json()["detail"].lower()


def test_calculate_injection_import_os() -> None:
    """__import__('os').system('ls') must be rejected with 400."""
    resp = client.post(
        "/calculate",
        json={"expression": "__import__('os').system('ls')"},
    )
    assert resp.status_code == 400


def test_calculate_injection_eval() -> None:
    """eval('1+1') must be rejected with 400."""
    resp = client.post("/calculate", json={"expression": "eval('1+1')"})
    assert resp.status_code == 400


def test_calculate_float_expression() -> None:
    """Float literals in expression."""
    resp = client.post("/calculate", json={"expression": "1.5 * 2"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 3.0


def test_calculate_power_in_expression() -> None:
    """2 ** 10 in expression."""
    resp = client.post("/calculate", json={"expression": "2 ** 10"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 1024


def test_calculate_expression_too_long() -> None:
    """Expression over 200 chars returns 422."""
    long_expr = "1" + " + 1" * 100  # well over 200 chars
    resp = client.post("/calculate", json={"expression": long_expr})
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# /history
# ---------------------------------------------------------------------------

def test_history_records_calculations() -> None:
    """Successful calculations appear in history."""
    _reset_history()
    client.post("/add", json={"a": 1, "b": 2})
    client.post("/calculate", json={"expression": "3 + 4"})

    resp = client.get("/history")
    assert resp.status_code == 200
    entries = resp.json()
    assert len(entries) == 2
    # Newest first
    assert entries[0]["operation"] == "calculate"
    assert entries[1]["operation"] == "add"
    assert "timestamp" in entries[0]


def test_history_limit_20() -> None:
    """Only the last 20 entries are kept."""
    _reset_history()
    for i in range(25):
        client.post("/add", json={"a": i, "b": 0})

    resp = client.get("/history")
    assert resp.status_code == 200
    entries = resp.json()
    assert len(entries) == 20
    # Newest first: the last one added was i=24
    assert entries[0]["result"] == 24


def test_history_empty() -> None:
    """Empty history returns an empty list."""
    _reset_history()
    resp = client.get("/history")
    assert resp.status_code == 200
    assert resp.json() == []


# ---------------------------------------------------------------------------
# Overflow / precision
# ---------------------------------------------------------------------------

def test_calculate_nested_power_overflow() -> None:
    """Nested powers like 2**2**2**2**2 can produce huge numbers → 400."""
    resp = client.post("/calculate", json={"expression": "2 ** 2 ** 2 ** 2 ** 2"})
    assert resp.status_code == 400


def test_float_precision() -> None:
    """0.1 + 0.2 must return 0.3, not 0.30000000000000004."""
    resp = client.post("/calculate", json={"expression": "0.1 + 0.2"})
    assert resp.status_code == 200
    assert resp.json()["result"] == 0.3


def test_get_index_returns_html() -> None:
    """GET / should return 200 with text/html content and calculator markup."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers.get("content-type", "")
    assert "<!DOCTYPE html>" in resp.text
    assert "Calculator" in resp.text
