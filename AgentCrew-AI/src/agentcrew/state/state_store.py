
from __future__ import annotations

from agentcrew.models import (
    AgentResult,
    AgentTask,
    TaskStatus,
)


class StateStore:
    def __init__(self, tasks: list[AgentTask]):
        self.statuses: dict[str, TaskStatus] = {
            task.task_id: TaskStatus.PENDING
            for task in tasks
        }

        self.results: dict[str, AgentResult] = {}

    def set_status(
        self,
        task_id: str,
        status: TaskStatus,
    ) -> None:
        allowed = {
            TaskStatus.PENDING: {
                TaskStatus.READY,
                TaskStatus.BLOCKED,
            },
            TaskStatus.READY: {
                TaskStatus.RUNNING,
                TaskStatus.BLOCKED,
            },
            TaskStatus.RUNNING: {
                TaskStatus.COMPLETED,
                TaskStatus.FAILED,
            },
            TaskStatus.COMPLETED: set(),
            TaskStatus.FAILED: set(),
            TaskStatus.BLOCKED: set(),
        }

        current = self.statuses[task_id]

        if status not in allowed[current]:
            raise ValueError(
                f"Invalid state transition: "
                f"{current.value} -> {status.value}"
            )

        self.statuses[task_id] = status

    def save_result(
        self,
        result: AgentResult,
    ) -> None:
        if result.task_id not in self.statuses:
            raise KeyError(result.task_id)

        self.results[result.task_id] = result

    def completed(self, task_id: str) -> bool:
        return (
            self.statuses[task_id]
            == TaskStatus.COMPLETED
        )
