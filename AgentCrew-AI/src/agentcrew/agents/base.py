
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from agentcrew.llm.client import LLMClient
from agentcrew.models import AgentResult, AgentTask


class BaseAgent(ABC):
    role: str = "base"

    def __init__(
        self,
        llm: LLMClient,
        tools: Any = None,
    ):
        self.llm = llm
        self.tools = tools

    @abstractmethod
    async def execute(
        self,
        task: AgentTask,
        context: dict[str, Any],
    ) -> AgentResult:
        raise NotImplementedError

    def result(
        self,
        task: AgentTask,
        output: dict[str, Any],
        success: bool = True,
        error: str | None = None,
    ) -> AgentResult:
        return AgentResult(
            task_id=task.task_id,
            agent_name=self.role,
            success=success,
            output=output,
            error=error,
        )
