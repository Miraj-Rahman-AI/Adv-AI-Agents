
from __future__ import annotations

from agentcrew.models import AgentResult, AgentTask


class SharedContext:
    def __init__(
        self,
        objective: str,
        coordination: dict | None = None,
    ):
        self.objective = objective
        self.coordination = coordination or {}

    def snapshot(
        self,
        task: AgentTask,
        results: dict[str, AgentResult],
    ) -> dict:
        """Share only the outputs of declared dependencies."""

        dependency_results = {}

        for dependency in task.dependencies:
            result = results.get(dependency)

            if result is not None:
                dependency_results[dependency] = {
                    "success": result.success,
                    "output": result.output,
                }

        return {
            "objective": self.objective,
            "coordination": dict(self.coordination),
            "results": dependency_results,
        }
