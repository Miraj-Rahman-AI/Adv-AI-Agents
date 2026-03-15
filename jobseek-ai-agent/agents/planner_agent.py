from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from config.constants import DEFAULT_JOB_QUERIES
from config.settings import Settings


@dataclass
class PlanStep:
    """Represents one executable step in the agent plan."""
    step_id: int
    name: str
    description: str


@dataclass
class ExecutionPlan:
    """Represents the full plan for the job search pipeline."""
    goal: str
    target_job_count: int
    queries: List[str] = field(default_factory=list)
    steps: List[PlanStep] = field(default_factory=list)


class PlannerAgent:
    """
    Planner agent responsible for decomposing the high-level user goal
    into structured steps and initial search queries.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def build_plan(self, goal: str) -> ExecutionPlan:
        """
        Build an execution plan from the user goal.
        """
        queries = self._generate_initial_queries(goal)
        steps = self._generate_steps()

        return ExecutionPlan(
            goal=goal,
            target_job_count=self.settings.target_job_count,
            queries=queries,
            steps=steps,
        )

    def _generate_initial_queries(self, goal: str) -> List[str]:
        """
        Generate initial search queries.
        For now, this uses predefined queries; later this can be replaced
        with an LLM-based planning module.
        """
        goal_lower = goal.lower()

        if "ai engineer" in goal_lower:
            return DEFAULT_JOB_QUERIES.copy()

        return [
            goal,
            *DEFAULT_JOB_QUERIES[:4],
        ]

    @staticmethod
    def _generate_steps() -> List[PlanStep]:
        """
        Define the default pipeline steps for the autonomous agent.
        """
        return [
            PlanStep(
                step_id=1,
                name="Search",
                description="Search recruitment platforms using initial keyword queries."
            ),
            PlanStep(
                step_id=2,
                name="Scrape",
                description="Fetch job listing pages and extract raw HTML or page content."
            ),
            PlanStep(
                step_id=3,
                name="Parse",
                description="Parse job postings into structured job records."
            ),
            PlanStep(
                step_id=4,
                name="Classify",
                description="Filter postings to keep only AI Engineer-related roles."
            ),
            PlanStep(
                step_id=5,
                name="Extract Skills",
                description="Extract technical tags and summarize core requirements."
            ),
            PlanStep(
                step_id=6,
                name="Deduplicate",
                description="Remove duplicate or near-duplicate job postings."
            ),
            PlanStep(
                step_id=7,
                name="Export",
                description="Export final structured results to JSON and CSV."
            ),
        ]

    @staticmethod
    def pretty_print(plan: ExecutionPlan) -> None:
        """
        Print the execution plan in a human-readable format.
        """
        print("=" * 60)
        print("Execution Plan")
        print("=" * 60)
        print(f"Goal: {plan.goal}")
        print(f"Target Job Count: {plan.target_job_count}")
        print("\nInitial Queries:")
        for idx, query in enumerate(plan.queries, start=1):
            print(f"  {idx}. {query}")

        print("\nPlanned Steps:")
        for step in plan.steps:
            print(f"  [{step.step_id}] {step.name}: {step.description}")
        print("=" * 60)
