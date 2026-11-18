"""Safe expression parser using Python's ast module.

Only allows: BinOp, UnaryOp, Constant (int/float) and the operators
+, -, *, /, **.  Everything else raises ValueError.
"""

import ast
from typing import Any


# Map of allowed ast operator nodes to Python operations.
_ALLOWED_OPS = {
    ast.Add: "add",
    ast.Sub: "subtract",
    ast.Mult: "multiply",
    ast.Div: "divide",
    ast.Pow: "power",
}


class _SafeEvaluator(ast.NodeVisitor):
    """Evaluate a restricted subset of arithmetic AST nodes."""

    def visit_Constant(self, node: ast.Constant) -> float:
        """Return numeric constants (int or float only)."""
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError(f"Only numeric values are allowed, got {type(node.value).__name__}")

    def visit_BinOp(self, node: ast.BinOp) -> float:
        """Evaluate binary operations: + - * / **."""
        if not isinstance(node.op, tuple(_ALLOWED_OPS)):
            raise ValueError(f"Operator {type(node.op).__name__} is not allowed")
        left: float = self.visit(node.left)
        right: float = self.visit(node.right)
        return _apply_op(type(node.op), left, right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> float:
        """Evaluate unary minus only."""
        if not isinstance(node.op, ast.USub):
            raise ValueError(f"Unary operator {type(node.op).__name__} is not allowed")
        operand: float = self.visit(node.operand)
        return -operand

    # Disallow any other node type by default (NodeVisitor visits children).
    def generic_visit(self, node: Any) -> None:
        raise ValueError(f"Node type {type(node).__name__} is not allowed in expressions")


def _apply_op(op_type: type, left: float, right: float) -> float:
    """Apply a binary operator with divide-by-zero and overflow checks."""
    if op_type is ast.Div:
        if right == 0.0:
            raise ValueError("Division by zero is not allowed")
        return left / right
    if op_type is ast.Pow:
        if abs(right) > 1000:
            raise ValueError("Exponent absolute value must not exceed 1000")
        try:
            result = left ** right
        except OverflowError:
            raise ValueError("Power operation overflow")
        # Guard against runaway intermediate values (e.g. 2**2**2**2**2
        # evaluates right-to-left as 2**65536 before the outer ops).
        if abs(result) > 1e308:
            raise ValueError("Power operation overflow")
        return result
    if op_type is ast.Add:
        return left + right
    if op_type is ast.Sub:
        return left - right
    if op_type is ast.Mult:
        return left * right
    raise ValueError(f"Unknown operator {op_type.__name__}")


def safe_eval(expression: str) -> float:
    """Parse and evaluate a math expression safely.

    Args:
        expression: A string like "2 + 3 * 4" with +, -, *, /, **,
                    parentheses, unary minus, ints and floats.

    Returns:
        The numeric result as a float.

    Raises:
        ValueError: If the expression is empty, unsafe, or contains
                    disallowed constructs.
    """
    if not expression or not expression.strip():
        raise ValueError("Expression must not be empty")
    if len(expression) > 200:
        raise ValueError("Expression must not exceed 200 characters")

    try:
        tree = ast.parse(expression, mode="eval", type_comments=True)
    except SyntaxError as exc:
        raise ValueError(f"Invalid expression: {exc}") from None

    evaluator = _SafeEvaluator()
    result: float = evaluator.visit(tree.body)
    if isinstance(result, float):
        result = round(result, 10)
    return result
