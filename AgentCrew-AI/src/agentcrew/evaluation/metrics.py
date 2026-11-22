
from __future__ import annotations

from typing import Any

from agentcrew.models import TaskStatus


def compute_metrics(
    statuses: dict[str, TaskStatus],
    duration_seconds: float,
    message_count: int,
) -> dict[str, Any]:
    total = len(statuses)

    completed = sum(
        status == TaskStatus.COMPLETED
        for status in statuses.values()
    )

    failed = sum(
        status == TaskStatus.FAILED
        for status in statuses.values()
    )

    blocked = sum(
        status == TaskStatus.BLOCKED
        for status in statuses.values()
    )

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "failed_tasks": failed,
        "blocked_tasks": blocked,
        "task_completion_rate": (
            round(completed / total, 4)
            if total else 0.0
        ),
        "duration_seconds": round(
            duration_seconds, 4
        ),
        "messages_exchanged": message_count,
    }
