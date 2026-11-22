
from __future__ import annotations

from typing import Any

from agentcrew.agents.base import BaseAgent
from agentcrew.llm.client import request_json
from agentcrew.models import AgentResult, AgentTask


class AnalystAgent(BaseAgent):
    role = "analyst"

    async def execute(
        self,
        task: AgentTask,
        context: dict[str, Any],
    ) -> AgentResult:
        response = await request_json(
            self.llm,
            self.role,
            {
                "objective": context["objective"],
                "task": task.description,
                "dependency_results": context.get(
                    "results", {}
                ),
                "instructions": (
                    "Define analysis criteria and provide "
                    "only conclusions justified by the "
                    "available inputs. Clearly acknowledge "
                    "missing evidence."
                ),
                "output_schema": {
                    "analysis": "string",
                    "criteria": ["string"],
                    "limitations": "string",
                },
            },
        )

        criteria = response.get("criteria")

        if not isinstance(criteria, list) or not criteria:
            raise ValueError(
                "Analyst must provide analysis criteria"
            )

        return self.result(
            task,
            {
                "analysis": str(
                    response.get("analysis", "")
                ),
                "criteria": criteria,
                "limitations": str(
                    response.get("limitations", "")
                ),
            },
        )
