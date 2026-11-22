
from __future__ import annotations

from agentcrew.models import AgentTask


class TaskManager:
    def __init__(
        self,
        allowed_roles: set[str],
        max_tasks: int = 12,
    ):
        self.allowed_roles = allowed_roles
        self.max_tasks = max_tasks

    def validate(
        self,
        tasks: list[AgentTask],
    ) -> dict[str, AgentTask]:
        if not tasks:
            raise ValueError("Task plan cannot be empty")

        if len(tasks) > self.max_tasks:
            raise ValueError(
                "Task plan exceeds maximum task count"
            )

        mapping: dict[str, AgentTask] = {}

        for task in tasks:
            if task.task_id in mapping:
                raise ValueError(
                    f"Duplicate task ID: {task.task_id}"
                )

            if task.agent_role not in self.allowed_roles:
                raise ValueError(
                    f"Unrecognized agent role: {task.agent_role}"
                )

            if len(task.dependencies) != len(
                set(task.dependencies)
            ):
                raise ValueError(
                    f"Duplicate dependencies: {task.task_id}"
                )

            mapping[task.task_id] = task

        for task in tasks:
            for dependency in task.dependencies:
                if dependency not in mapping:
                    raise ValueError(
                        f"Unknown dependency: {dependency}"
                    )

                if dependency == task.task_id:
                    raise ValueError(
                        "A task cannot depend on itself"
                    )

        visited = set()
        visiting = set()

        def visit(task_id: str) -> None:
            if task_id in visiting:
                raise ValueError(
                    "Circular task dependency detected"
                )

            if task_id in visited:
                return

            visiting.add(task_id)

            for dependency in mapping[
                task_id
            ].dependencies:
                visit(dependency)

            visiting.remove(task_id)
            visited.add(task_id)

        for task in tasks:
            visit(task.task_id)

        return mapping
