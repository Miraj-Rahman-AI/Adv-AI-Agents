
from __future__ import annotations

from typing import Any

from agentcrew.agents.base import BaseAgent
from agentcrew.llm.client import request_json
from agentcrew.models import AgentResult, AgentTask


class SynthesisAgent(BaseAgent):
    role = "synthesizer"

    async def execute(
        self,
        task: AgentTask,
        context: dict[str, Any],
    ) -> AgentResult:
        results = context.get("results", {})
        review = results.get("review", {}).get(
            "output", {}
        )

        if review.get("approved") is not True:
            return self.result(
                task,
                {},
                success=False,
                error="Review approval required",
            )

        response = await request_json(
            self.llm,
            self.role,
            {
                "objective": context["objective"],
                "results": results,
                "instructions": (
                    "Create a concise evidence-based report. "
                    "Do not invent research sources. "
                    "Explain unresolved limitations."
                ),
                "output_schema": {
                    "report": "Markdown report text",
                },
            },
        )

        report = response.get("report")

        if not isinstance(report, str) or not report.strip():
            raise ValueError(
                "Synthesizer returned an empty report"
            )

        return self.result(
            task,
            {"report": report},
        )
