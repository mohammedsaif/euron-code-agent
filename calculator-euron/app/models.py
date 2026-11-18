"""Pydantic v2 request and response models for the Calculator API."""

from pydantic import BaseModel, Field


class OperandsRequest(BaseModel):
    """Request body for binary math endpoints (/add, /subtract, etc.)."""

    a: float = Field(description="First operand (int or float)")
    b: float = Field(description="Second operand (int or float)")


class CalculateRequest(BaseModel):
    """Request body for the /calculate expression endpoint."""

    expression: str = Field(
        min_length=1,
        max_length=200,
        description="Mathematical expression string, e.g. '2 + 3 * 4'",
    )


class MathResponse(BaseModel):
    """Response for binary math endpoints."""

    operation: str
    a: float
    b: float
    result: float


class CalculateResponse(BaseModel):
    """Response for the /calculate endpoint."""

    expression: str
    result: float


class HistoryEntry(BaseModel):
    """One item in the calculation history."""

    operation: str
    input: str
    result: float
    timestamp: str
