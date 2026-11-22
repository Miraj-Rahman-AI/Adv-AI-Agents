
from __future__ import annotations

from typing import Any

from agentcrew.agents.base import BaseAgent
from agentcrew.llm.client import request_json
from agentcrew.models import AgentResult, AgentTask


class CoordinatorAgent(BaseAgent):
    role = "coordinator"

    async def execute(
        self,
        task: AgentTask,
        context: dict[str, Any],
    ) -> AgentResult:
        objective = context["objective"]

        response = await request_json(
            self.llm,
            self.role,
            {
                "objective": objective,
                "instructions": (
                    "Interpret the user's goal. "
                    "Do not invent additional authorization."
                ),
                "output_schema": {
                    "goal": "string",
                    "success_criteria": ["string"],
                },
            },
        )

        goal = response.get("goal")
        criteria = response.get("success_criteria")

        if not isinstance(goal, str) or not goal.strip():
            raise ValueError("Coordinator returned no goal")

        if not isinstance(criteria, list):
            raise ValueError(
                "Coordinator returned invalid criteria"
            )

        return self.result(
            task,
            {
                "goal": goal,
                "success_criteria": criteria,
            },
        )
