
from __future__ import annotations

import time
from typing import Any

from agentcrew.communication.message_bus import MessageBus
from agentcrew.config import Settings
from agentcrew.evaluation.metrics import compute_metrics
from agentcrew.models import (
    AgentTask,
    ExecutionReport,
    TaskStatus,
)
from agentcrew.observability.tracing import TraceRecorder
from agentcrew.orchestration.scheduler import TaskScheduler
from agentcrew.orchestration.task_manager import TaskManager
from agentcrew.state.shared_context import SharedContext


class AgentCrewWorkflow:
    def __init__(
        self,
        agents: dict[str, Any],
        settings: Settings,
        message_bus: MessageBus,
        tracer: TraceRecorder,
    ):
        self.agents = agents
        self.settings = settings
        self.message_bus = message_bus
        self.tracer = tracer

    async def run(
        self,
        objective: str,
    ) -> ExecutionReport:
        started = time.perf_counter()

        try:
            if not objective.strip():
                raise ValueError(
                    "User objective cannot be empty"
                )

            self.tracer.record(
                "workflow_started"
            )

            coordinator_task = AgentTask(
                task_id="coordination",
                description="Interpret the objective",
                agent_role="coordinator",
            )

            coordination = await self.agents[
                "coordinator"
            ].execute(
                coordinator_task,
                {"objective": objective},
            )

            if not coordination.success:
                raise RuntimeError(
                    "Coordinator failed"
                )

            planner_task = AgentTask(
                task_id="planning",
                description="Generate the task plan",
                agent_role="planner",
            )

            planning = await self.agents[
                "planner"
            ].execute(
                planner_task,
                {
                    "objective": objective,
                    "coordination": coordination.output,
                },
            )

            if not planning.success:
                raise RuntimeError(
                    "Planner failed"
                )

            raw_tasks = planning.output["tasks"]

            tasks = [
                AgentTask.from_dict(task)
                for task in raw_tasks
            ]

            allowed_roles = (
                set(self.agents)
                - {"coordinator", "planner"}
            )

            task_manager = TaskManager(
                allowed_roles=allowed_roles,
                max_tasks=self.settings.max_tasks,
            )

            task_manager.validate(tasks)

            # This first implementation has one canonical
            # review task followed by one synthesis task.
            roles = {
                task.task_id: task.agent_role
                for task in tasks
            }

            if roles.get("review") != "reviewer":
                raise ValueError(
                    "Plan requires a reviewer task "
                    "with ID 'review'"
                )

            if roles.get("synthesis") != "synthesizer":
                raise ValueError(
                    "Plan requires a synthesizer task "
                    "with ID 'synthesis'"
                )

            synthesis_task = next(
                task
                for task in tasks
                if task.task_id == "synthesis"
            )

            if "review" not in synthesis_task.dependencies:
                raise ValueError(
                    "Synthesis must depend on review"
                )

            shared = SharedContext(
                objective=objective,
                coordination=coordination.output,
            )

            scheduler = TaskScheduler(
                agents=self.agents,
                max_concurrency=self.settings.max_concurrency,
                max_retries=self.settings.max_retries,
                task_timeout=self.settings.task_timeout,
                message_bus=self.message_bus,
                tracer=self.tracer,
            )

            store = await scheduler.run(tasks, shared)

            final_result = store.results.get(
                "synthesis"
            )

            complete = all(
                status == TaskStatus.COMPLETED
                for status in store.statuses.values()
            )

            final_output = (
                final_result.output.get("report", "")
                if final_result and final_result.success
                else (
                    "The workflow did not fully complete. "
                    "See task states and errors."
                )
            )

            errors = [
                f"{task_id}: {result.error}"
                for task_id, result in store.results.items()
                if not result.success
            ]

            errors.extend(
                f"{task_id}: blocked by a failed dependency"
                for task_id, status in store.statuses.items()
                if status == TaskStatus.BLOCKED
            )

            duration = time.perf_counter() - started

            metrics = compute_metrics(
                statuses=store.statuses,
                duration_seconds=duration,
                message_count=self.message_bus.count(),
            )

            self.tracer.record(
                "workflow_finished",
                status=(
                    "completed" if complete else "partial"
                ),
            )

            return ExecutionReport(
                objective=objective,
                status=(
                    "completed" if complete else "partial"
                ),
                final_output=final_output,
                results=store.results,
                task_states=store.statuses,
                duration_seconds=duration,
                metrics=metrics,
                errors=errors,
            )

        except Exception as error:
            duration = time.perf_counter() - started

            self.tracer.record(
                "workflow_failed",
                error=(
                    f"{type(error).__name__}: {error}"
                ),
            )

            return ExecutionReport(
                objective=objective,
                status="failed",
                final_output=(
                    "Workflow initialization or "
                    "planning failed."
                ),
                results={},
                task_states={},
                duration_seconds=duration,
                errors=[
                    f"{type(error).__name__}: {error}"
                ],
            )
