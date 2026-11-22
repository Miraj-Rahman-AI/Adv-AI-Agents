
from __future__ import annotations

import asyncio
import inspect
from typing import Any

from agentcrew.security.permissions import (
    AuthorizationContext,
)
from agentcrew.security.policy_engine import PolicyEngine
from agentcrew.tools.registry import ToolRegistry


class ToolExecutor:
    def __init__(
        self,
        registry: ToolRegistry,
        policy: PolicyEngine,
        authorization: AuthorizationContext,
        tracer: Any = None,
    ):
        self.registry = registry
        self.policy = policy
        self.authorization = authorization
        self.tracer = tracer

    async def execute(
        self,
        role: str,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> Any:
        definition = self.registry.get(tool_name)

        if not isinstance(arguments, dict):
            raise ValueError(
                "Tool arguments must be an object"
            )

        try:
            self.policy.authorize(
                role=role,
                tool_name=definition.name,
                action=definition.action,
                resource=definition.resource,
                authorization=self.authorization,
            )

            if not set(arguments).issubset(
                definition.allowed_arguments
            ):
                raise ValueError(
                    "Tool contains unexpected arguments"
                )

            inspect.signature(
                definition.handler
            ).bind(**arguments)

        except (PermissionError, ValueError, TypeError):
            if self.tracer:
                self.tracer.record(
                    "tool_rejected",
                    role=role,
                    tool=tool_name,
                )
            raise

        if self.tracer:
            self.tracer.record(
                "tool_started",
                role=role,
                tool=tool_name,
            )

        if inspect.iscoroutinefunction(
            definition.handler
        ):
            result = await definition.handler(**arguments)
        else:
            result = await asyncio.to_thread(
                definition.handler,
                **arguments,
            )

        if self.tracer:
            self.tracer.record(
                "tool_completed",
                role=role,
                tool=tool_name,
            )

        return result
