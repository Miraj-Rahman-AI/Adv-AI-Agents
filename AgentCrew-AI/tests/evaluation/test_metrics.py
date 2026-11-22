
from agentcrew.evaluation.metrics import compute_metrics
from agentcrew.models import TaskStatus


def test_metrics_calculation():
    statuses = {
        "t1": TaskStatus.COMPLETED,
        "t2": TaskStatus.COMPLETED,
        "t3": TaskStatus.FAILED,
        "t4": TaskStatus.BLOCKED,
    }

    metrics = compute_metrics(
        statuses=statuses,
        duration_seconds=2.5,
        message_count=6,
    )

    assert metrics["total_tasks"] == 4
    assert metrics["completed_tasks"] == 2
    assert metrics["failed_tasks"] == 1
    assert metrics["blocked_tasks"] == 1
    assert metrics["task_completion_rate"] == 0.5
    assert metrics["messages_exchanged"] == 6
