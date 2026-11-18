"""In-memory calculation history store.

Keeps the last 20 calculations in a collections.deque with maxlen=20.
"""

from collections import deque
from datetime import datetime, timezone

from .models import HistoryEntry

# Shared history buffer – newest item appended last.
_history: deque[HistoryEntry] = deque(maxlen=20)


def record(operation: str, input_str: str, result: float) -> None:
    """Record a successful calculation in the history buffer.

    Args:
        operation: Human-readable operation name (e.g. "add", "calculate").
        input_str:  The original input description (e.g. "2 + 3" or "2 + 3 * 4").
        result:     The numeric result.
    """
    entry = HistoryEntry(
        operation=operation,
        input=input_str,
        result=result,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    _history.append(entry)


def get_history() -> list[HistoryEntry]:
    """Return the last 20 entries, newest first."""
    return list(reversed(_history))


def clear() -> None:
    """Clear the history. Only for testing."""
    _history.clear()
