
from __future__ import annotations

import asyncio
from typing import Any

from agentcrew.communication.message_bus import MessageBus
from agentcrew.models import (
    AgentResult,
    AgentTask,
    TaskStatus,
)
from agentcrew.observability.tracing import TraceRecorder
from agentcrew.orchestration.task_manager import TaskManager
from agentcrew.state.shared_context import SharedContext
from agentcrew.state.state_store import StateStore


class TaskScheduler:
    def __init__(
        self,
        agents: dict[str, Any],
        max_concurrency: int,
        max_retries: int,
        task_timeout: float,
        message_bus: MessageBus,
        tracer: TraceRecorder,
    ):
        if max_concurrency < 1:
            raise ValueError(
                "max_concurrency must be positive"
            )

        if max_retries < 0:
            raise ValueError(
                "max_retries cannot be negative"
            )

        if task_timeout <= 0:
            raise ValueError(
                "task_timeout must be positive"
            )

        self.agents = agents
        self.max_retries = max_retries
        self.task_timeout = task_timeout
        self.semaphore = asyncio.Semaphore(
            max_concurrency
        )
        self.message_bus = message_bus
        self.tracer = tracer

    async def _execute_task(
        self,
        task: AgentTask,
        shared: SharedContext,
        store: StateStore,
    ) -> None:
        async with self.semaphore:
            store.set_status(
                task.task_id,
                TaskStatus.RUNNING,
            )

            self.tracer.record(
                "task_started",
                task_id=task.task_id,
                role=task.agent_role,
            )

            context = shared.snapshot(
                task,
                store.results,
            )

            result = None

            for attempt in range(
                1, self.max_retries + 2
            ):
                try:
                    result = await asyncio.wait_for(
                        self.agents[
                            task.agent_role
                        ].execute(task, context),
                        timeout=self.task_timeout,
                    )

                    if not isinstance(
                        result, AgentResult
                    ):
                        raise TypeError(
                            "Agent did not return AgentResult"
                        )

                    if result.task_id != task.task_id:
                        raise ValueError(
                            "Agent returned incorrect task ID"
                        )

                    if not isinstance(
                        result.output, dict
                    ):
                        raise ValueError(
                            "Agent output must be an object"
                        )

                except Exception as error:
                    result = AgentResult(
                        task_id=task.task_id,
                        agent_name=task.agent_role,
                        success=False,
                        error=(
                            f"{type(error).__name__}: {error}"
                        ),
                    )

                result.attempts = attempt

                if result.success:
                    break

                self.tracer.record(
                    "task_attempt_failed",
                    task_id=task.task_id,
                    attempt=attempt,
                    error=result.error,
                )

            assert result is not None

            store.save_result(result)

            status = (
                TaskStatus.COMPLETED
                if result.success
                else TaskStatus.FAILED
            )

            store.set_status(task.task_id, status)

            self.message_bus.publish(
                sender=task.agent_role,
                recipient="orchestrator",
                message_type="task_result",
                task_id=task.task_id,
                payload={
                    "success": result.success,
                    "attempts": result.attempts,
                    "error": result.error,
                },
            )

            self.tracer.record(
                "task_finished",
                task_id=task.task_id,
                status=status.value,
                attempts=result.attempts,
            )

    async def run(
        self,
        tasks: list[AgentTask],
        shared: SharedContext,
    ) -> StateStore:
        manager = TaskManager(
            allowed_roles=set(self.agents),
            max_tasks=len(tasks),
        )

        task_map = manager.validate(tasks)
        store = StateStore(tasks)

        pending = set(task_map)

        while pending:
            # Block tasks whose dependencies failed.
            for task_id in sorted(list(pending)):
                task = task_map[task_id]

                dependency_failed = any(
                    store.statuses[dependency]
                    in {
                        TaskStatus.FAILED,
                        TaskStatus.BLOCKED,
                    }
                    for dependency in task.dependencies
                )

                if dependency_failed:
                    store.set_status(
                        task_id,
                        TaskStatus.BLOCKED,
                    )
                    pending.remove(task_id)

                    self.tracer.record(
                        "task_blocked",
                        task_id=task_id,
                    )

            if not pending:
                break

            ready = [
                task_map[task_id]
                for task_id in sorted(pending)
                if all(
                    store.statuses[dependency]
                    == TaskStatus.COMPLETED
                    for dependency in task_map[
                        task_id
                    ].dependencies
                )
            ]

            if not ready:
                raise RuntimeError(
                    "No executable tasks remain; "
                    "check task dependencies"
                )

            for task in ready:
                store.set_status(
                    task.task_id,
                    TaskStatus.READY,
                )

                self.message_bus.publish(
                    sender="orchestrator",
                    recipient=task.agent_role,
                    message_type="task_assignment",
                    task_id=task.task_id,
                    payload={
                        "description": task.description,
                    },
                )

            await asyncio.gather(
                *[
                    self._execute_task(
                        task,
                        shared,
                        store,
                    )
                    for task in ready
                ]
            )

            for task in ready:
                pending.remove(task.task_id)

        return store
