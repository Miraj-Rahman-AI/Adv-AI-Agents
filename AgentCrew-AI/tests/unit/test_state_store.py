
import pytest

from agentcrew.models import AgentTask, TaskStatus
from agentcrew.state import StateStore


def test_valid_state_transitions():
    task = AgentTask(
        task_id="t1",
        description="Test task",
        agent_role="researcher",
    )

    store = StateStore([task])

    store.set_status("t1", TaskStatus.READY)
    store.set_status("t1", TaskStatus.RUNNING)
    store.set_status("t1", TaskStatus.COMPLETED)

    assert store.completed("t1")


def test_invalid_state_transition():
    task = AgentTask(
        task_id="t1",
        description="Test task",
        agent_role="researcher",
    )

    store = StateStore([task])

    with pytest.raises(ValueError):
        store.set_status(
            "t1",
            TaskStatus.COMPLETED,
        )
