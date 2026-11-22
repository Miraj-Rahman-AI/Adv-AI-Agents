
import pytest

from agentcrew.models import AgentTask
from agentcrew.orchestration.task_manager import (
    TaskManager,
)


def make_task(
    task_id: str,
    dependencies: tuple[str, ...] = (),
) -> AgentTask:
    return AgentTask(
        task_id=task_id,
        description=f"Execute {task_id}",
        agent_role="researcher",
        dependencies=dependencies,
    )


def test_valid_task_graph():
    manager = TaskManager(
        {"researcher"},
        max_tasks=5,
    )

    tasks = [
        make_task("t1"),
        make_task("t2", ("t1",)),
        make_task("t3", ("t2",)),
    ]

    graph = manager.validate(tasks)

    assert len(graph) == 3
    assert graph["t3"].dependencies == ("t2",)


def test_duplicate_task_ids():
    manager = TaskManager({"researcher"})

    with pytest.raises(ValueError):
        manager.validate([
            make_task("t1"),
            make_task("t1"),
        ])


def test_missing_dependency():
    manager = TaskManager({"researcher"})

    with pytest.raises(ValueError):
        manager.validate([
            make_task("t1", ("missing",)),
        ])


def test_circular_dependency():
    manager = TaskManager({"researcher"})

    tasks = [
        make_task("a", ("b",)),
        make_task("b", ("a",)),
    ]

    with pytest.raises(
        ValueError,
        match="Circular",
    ):
        manager.validate(tasks)


def test_unknown_role():
    manager = TaskManager({"researcher"})

    task = AgentTask(
        task_id="t1",
        description="Unknown role",
        agent_role="administrator",
    )

    with pytest.raises(ValueError):
        manager.validate([task])
