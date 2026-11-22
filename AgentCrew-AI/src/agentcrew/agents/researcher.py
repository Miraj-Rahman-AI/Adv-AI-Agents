
from __future__ import annotations

from typing import Any

from agentcrew.agents.base import BaseAgent
from agentcrew.llm.client import request_json
from agentcrew.models import AgentResult, AgentTask


class ResearchAgent(BaseAgent):
    role = "researcher"

    async def execute(
        self,
        task: AgentTask,
        context: dict[str, Any],
    ) -> AgentResult:
        if self.tools is None:
            raise RuntimeError(
                "Research agent has no tool executor"
            )

        objective = context["objective"]

        sources = await self.tools.execute(
            role=self.role,
            tool_name="document_search",
            arguments={
                "query": objective,
                "limit": 3,
            },
        )

        if not sources:
            return self.result(
                task,
                {
                    "summary": "No matching documents found",
                    "sources": [],
                    "findings": [],
                },
                success=False,
                error="No supporting local documents found",
            )

        response = await request_json(
            self.llm,
            self.role,
            {
                "objective": objective,
                "sources": sources,
                "instructions": (
                    "Summarize only supported findings. "
                    "Each finding must cite a source identifier "
                    "from the supplied sources. "
                    "Do not fabricate references."
                ),
                "output_schema": {
                    "summary": "string",
                    "findings": [
                        {
                            "claim": "string",
                            "source": "source identifier",
                        }
                    ],
                },
            },
        )

        findings = response.get("findings", [])

        if not isinstance(findings, list):
            raise ValueError(
                "Research findings must be a list"
            )

        return self.result(
            task,
            {
                "summary": str(
                    response.get("summary", "")
                ),
                "sources": sources,
                "findings": findings,
            },
        )
