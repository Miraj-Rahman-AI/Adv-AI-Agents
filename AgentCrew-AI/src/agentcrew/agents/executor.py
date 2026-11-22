
from __future__ import annotations

from typing import Any

from agentcrew.agents.base import BaseAgent
from agentcrew.models import AgentResult, AgentTask


class ExecutionAgent(BaseAgent):
    role = "executor"

    async def execute(
        self,
        task: AgentTask,
        context: dict[str, Any],
    ) -> AgentResult:
        if self.tools is None:
            raise RuntimeError(
                "Execution agent has no tool executor"
            )

        tool_name = task.payload.get("tool")
        arguments = task.payload.get("arguments", {})

        if not isinstance(tool_name, str):
            raise ValueError(
                "Execution task requires a tool name"
            )

        if not isinstance(arguments, dict):
            raise ValueError(
                "Execution arguments must be an object"
            )

        output = await self.tools.execute(
            role=self.role,
            tool_name=tool_name,
            arguments=arguments,
        )

        return self.result(
            task,
            {
                "tool": tool_name,
                "result": output,
            },
        )
