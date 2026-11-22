
from __future__ import annotations

from typing import Any

from agentcrew.agents.base import BaseAgent
from agentcrew.llm.client import request_json
from agentcrew.models import AgentResult, AgentTask


class PlannerAgent(BaseAgent):
    role = "planner"

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
                "coordination": context.get(
                    "coordination", {}
                ),
                "instructions": (
                    "Produce a valid dependency-aware plan. "
                    "Use these agent roles only: researcher, "
                    "executor, analyst, reviewer, synthesizer. "
                    "Include research, analysis, review, and "
                    "synthesis. Ensure synthesis depends on "
                    "review. Make research and criteria analysis "
                    "independent where possible. "
                    "Do not invent tool permissions."
                ),
                "output_schema": {
                    "tasks": [
                        {
                            "task_id": "string",
                            "agent_role": "string",
                            "description": "string",
                            "dependencies": ["task_id"],
                            "payload": {},
                        }
                    ]
                },
            },
        )

        tasks = response.get("tasks")

        if not isinstance(tasks, list) or not tasks:
            raise ValueError(
                "Planner must return a non-empty task list"
            )

        return self.result(task, {"tasks": tasks})
