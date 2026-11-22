
from __future__ import annotations

from typing import Any

from agentcrew.security.permissions import (
    AuthorizationContext,
)


class PolicyEngine:
    def __init__(
        self,
        agent_rules: dict[str, Any],
        tool_rules: dict[str, Any],
    ):
        self.agent_rules = agent_rules
        self.tool_rules = tool_rules

    def authorize(
        self,
        role: str,
        tool_name: str,
        action: str,
        resource: str,
        authorization: AuthorizationContext,
    ) -> None:
        agent = self.agent_rules.get(role)
        rule = self.tool_rules.get(tool_name)

        if not isinstance(agent, dict):
            raise PermissionError(
                f"Unknown or disabled agent role: {role}"
            )

        if not isinstance(rule, dict):
            raise PermissionError(
                f"Tool not configured: {tool_name}"
            )

        if tool_name not in agent.get("tools", []):
            raise PermissionError(
                f"Agent {role} cannot use {tool_name}"
            )

        if role not in rule.get("allowed_roles", []):
            raise PermissionError(
                f"Tool {tool_name} does not allow role {role}"
            )

        if rule.get("action") != action:
            raise PermissionError(
                "Tool action does not match trusted policy"
            )

        if rule.get("resource") != resource:
            raise PermissionError(
                "Tool resource does not match trusted policy"
            )

        if tool_name not in authorization.allowed_tools:
            raise PermissionError(
                f"Tool not authorized: {tool_name}"
            )

        if action not in authorization.allowed_actions:
            raise PermissionError(
                f"Action not authorized: {action}"
            )

        if resource not in authorization.allowed_resources:
            raise PermissionError(
                f"Resource not authorized: {resource}"
            )
