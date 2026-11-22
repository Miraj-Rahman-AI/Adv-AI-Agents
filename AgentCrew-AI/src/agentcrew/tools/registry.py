
from __future__ import annotations

import ast
import math
import operator
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass
class ToolDefinition:
    name: str
    description: str
    action: str
    resource: str
    handler: Callable[..., Any]
    allowed_arguments: frozenset[str]


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        if tool.name in self._tools:
            raise ValueError(
                f"Duplicate tool name: {tool.name}"
            )

        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")

        return self._tools[name]

    def list_tools(self) -> list[str]:
        return sorted(self._tools)


def load_documents(
    directory: Path,
    max_files: int = 100,
    max_chars: int = 30000,
) -> list[dict[str, str]]:
    """Load Markdown files from an approved directory."""

    root = directory.resolve()

    if not root.is_dir():
        return []

    documents = []

    for path in sorted(root.rglob("*.md")):
        if len(documents) >= max_files:
            break

        resolved = path.resolve()

        # Exclude symlinks escaping the approved directory.
        if not resolved.is_relative_to(root):
            continue

        if not resolved.is_file():
            continue

        try:
            with resolved.open(
                "r",
                encoding="utf-8",
            ) as handle:
                body = handle.read(max_chars)
        except (UnicodeError, OSError):
            continue

        documents.append(
            {
                "source": str(path.relative_to(root)),
                "title": path.stem,
                "body": body,
            }
        )

    return documents


def _terms(text: str) -> set[str]:
    stopwords = {
        "the", "and", "for", "with", "from",
        "this", "that", "about", "into",
        "what", "which", "using", "agent",
        "agents", "please", "compare",
    }

    words = re.findall(
        r"[a-zA-Z0-9_-]{3,}",
        text.lower(),
    )

    return set(words) - stopwords


def search_documents(
    documents: list[dict[str, str]],
    query: str,
    limit: int = 3,
) -> list[dict[str, Any]]:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query cannot be empty")

    if len(query) > 2000:
        raise ValueError("Search query is too long")

    if type(limit) is not int or not 1 <= limit <= 5:
        raise ValueError("limit must be between 1 and 5")

    query_terms = _terms(query)
    ranked = []

    for document in documents:
        body = document["body"]
        title = document["title"]

        text_terms = _terms(title + " " + body)
        score = len(query_terms & text_terms)

        if score <= 0:
            continue

        # Select a relevant local excerpt.
        lines = body.splitlines()
        matching_lines = [
            line.strip()
            for line in lines
            if _terms(line) & query_terms
        ]

        excerpt = " ".join(
            matching_lines[:5]
        ).strip()[:700]

        if not excerpt:
            excerpt = body[:700]

        ranked.append(
            {
                "source": document["source"],
                "title": title,
                "excerpt": excerpt,
                "score": score,
            }
        )

    ranked.sort(
        key=lambda item: (-item["score"], item["source"])
    )

    return ranked[:limit]


_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}

_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate(expression: str) -> float:
    """Evaluate restricted arithmetic without eval()."""

    if not isinstance(expression, str):
        raise ValueError("Expression must be a string")

    if not 1 <= len(expression) <= 100:
        raise ValueError("Invalid expression length")

    tree = ast.parse(expression, mode="eval")

    def evaluate(node: ast.AST, depth: int = 0) -> float:
        if depth > 20:
            raise ValueError("Expression nesting is too deep")

        if isinstance(node, ast.Expression):
            return evaluate(node.body, depth + 1)

        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Only numbers are allowed")

            result = float(node.value)

        elif isinstance(node, ast.BinOp):
            operation = _BINARY_OPERATORS.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError("Unsupported operator")

            left = evaluate(node.left, depth + 1)
            right = evaluate(node.right, depth + 1)

            result = operation(left, right)

        elif isinstance(node, ast.UnaryOp):
            operation = _UNARY_OPERATORS.get(
                type(node.op)
            )

            if operation is None:
                raise ValueError("Unsupported unary operator")

            result = operation(
                evaluate(node.operand, depth + 1)
            )

        else:
            raise ValueError(
                "Unsupported expression syntax"
            )

        if not math.isfinite(result):
            raise ValueError("Non-finite result")

        if abs(result) > 1e12:
            raise ValueError("Result exceeds safety limit")

        return result

    return evaluate(tree)


def build_default_registry(
    documents: list[dict[str, str]],
) -> ToolRegistry:
    registry = ToolRegistry()

    def document_search(
        query: str,
        limit: int = 3,
    ) -> list[dict[str, Any]]:
        return search_documents(
            documents=documents,
            query=query,
            limit=limit,
        )

    registry.register(
        ToolDefinition(
            name="document_search",
            description="Search approved local documents",
            action="read",
            resource="documents",
            handler=document_search,
            allowed_arguments=frozenset(
                {"query", "limit"}
            ),
        )
    )

    registry.register(
        ToolDefinition(
            name="calculator",
            description="Evaluate basic arithmetic",
            action="compute",
            resource="numbers",
            handler=calculate,
            allowed_arguments=frozenset(
                {"expression"}
            ),
        )
    )

    return registry
