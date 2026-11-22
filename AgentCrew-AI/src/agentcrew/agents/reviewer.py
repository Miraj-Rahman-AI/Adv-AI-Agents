
from __future__ import annotations

from typing import Any

from agentcrew.agents.base import BaseAgent
from agentcrew.llm.client import request_json
from agentcrew.models import AgentResult, AgentTask
from agentcrew.verification.validator import (
    validate_research_evidence,
)


class ReviewerAgent(BaseAgent):
    role = "reviewer"

    async def execute(
        self,
        task: AgentTask,
        context: dict[str, Any],
    ) -> AgentResult:
        results = context.get("results", {})

        issues = validate_research_evidence(results)

        analysis = results.get("analysis", {}).get(
            "output", {}
        )

        if not analysis.get("criteria"):
            issues.append(
                "Missing analysis criteria"
            )

        response = await request_json(
            self.llm,
            self.role,
            {
                "objective": context["objective"],
                "results": results,
                "instructions": (
                    "Review available evidence and analysis. "
                    "Approve only when the task requirements "
                    "are satisfied. Return approved as a JSON "
                    "boolean and issues as an array of strings."
                ),
                "output_schema": {
                    "approved": True,
                    "issues": ["string"],
                },
            },
        )

        model_issues = response.get("issues", [])

        if not isinstance(model_issues, list):
            raise ValueError(
                "Reviewer issues must be a list"
            )

        issues.extend(str(item) for item in model_issues)

        approved = (
            response.get("approved") is True
            and not issues
        )

        return self.result(
            task,
            {
                "approved": approved,
                "issues": issues,
            },
            success=approved,
            error=(
                "; ".join(issues) or "Review rejected"
                if not approved
                else None
            ),
        )
