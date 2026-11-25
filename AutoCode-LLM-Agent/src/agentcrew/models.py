
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class TaskStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class AgentTask:
    task_id: str
    description: str
    agent_role: str
    dependencies: tuple[str, ...] = ()
    payload: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentTask":
        if not isinstance(data, dict):
            raise ValueError("Task must be an object")

        task_id = data.get("task_id")
        description = data.get("description")
        role = data.get("agent_role")
        dependencies = data.get("dependencies", [])
        payload = data.get("payload", {})

        if not all(
            isinstance(v, str) and v.strip()
            for v in (task_id, description, role)
        ):
            raise ValueError(
                "Task requires task_id, description and agent_role"
            )

        if not isinstance(dependencies, (list, tuple)):
            raise ValueError("dependencies must be a list")

        if not all(isinstance(x, str) for x in dependencies):
            raise ValueError("Dependency identifiers must be strings")

        if not isinstance(payload, dict):
            raise ValueError("Task payload must be an object")

        return cls(
            task_id=task_id,
            description=description,
            agent_role=role,
            dependencies=tuple(dependencies),
            payload=payload,
        )


@dataclass
class AgentResult:
    task_id: str
    agent_name: str
    success: bool
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    attempts: int = 1


@dataclass
class ExecutionReport:
    objective: str
    status: str
    final_output: str
    results: dict[str, AgentResult]
    task_states: dict[str, TaskStatus]
    duration_seconds: float = 0.0
    metrics: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "objective": self.objective,
            "status": self.status,
            "final_output": self.final_output,
            "results": {
                key: asdict(value)
                for key, value in self.results.items()
            },
            "task_states": {
                key: value.value
                for key, value in self.task_states.items()
            },
            "duration_seconds": self.duration_seconds,
            "metrics": self.metrics,
            "errors": self.errors,
        }
