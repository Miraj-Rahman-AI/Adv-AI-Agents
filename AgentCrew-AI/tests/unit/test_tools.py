
import asyncio

import pytest

from agentcrew.security import (
    AuthorizationContext,
    PolicyEngine,
)
from agentcrew.tools import (
    ToolExecutor,
    build_default_registry,
)
from agentcrew.tools.registry import calculate


def test_calculator():
    assert calculate("2 + 3 * 4") == 14.0
    assert calculate("(12 - 4) / 2") == 4.0


def test_calculator_rejects_code():
    with pytest.raises((ValueError, SyntaxError)):
        calculate(
            "__import__('os').system('echo test')"
        )


def test_document_search():
    documents = [
        {
            "source": "research.md",
            "title": "Research",
            "body": (
                "Multi-agent orchestration supports "
                "dependency-aware task execution."
            ),
        }
    ]

    registry = build_default_registry(documents)
    tool = registry.get("document_search")

    result = tool.handler(
        query="dependency-aware orchestration"
    )

    assert len(result) == 1
    assert result[0]["source"] == "research.md"


def test_tool_executor_rejects_wrong_role():
    registry = build_default_registry([])

    policy = PolicyEngine(
        agent_rules={
            "analyst": {"tools": []}
        },
        tool_rules={
            "calculator": {
                "action": "compute",
                "resource": "numbers",
                "allowed_roles": ["executor"],
            }
        },
    )

    authorization = AuthorizationContext(
        allowed_tools=frozenset({"calculator"}),
        allowed_actions=frozenset({"compute"}),
        allowed_resources=frozenset({"numbers"}),
    )

    executor = ToolExecutor(
        registry,
        policy,
        authorization,
    )

    async def invoke():
        await executor.execute(
            role="analyst",
            tool_name="calculator",
            arguments={"expression": "2+2"},
        )

    with pytest.raises(PermissionError):
        asyncio.run(invoke())
