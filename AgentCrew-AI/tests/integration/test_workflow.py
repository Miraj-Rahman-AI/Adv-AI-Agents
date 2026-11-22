
import asyncio

from agentcrew.config import load_settings
from agentcrew.main import run_crew
from agentcrew.models import TaskStatus


def test_complete_mock_workflow(tmp_path):
    docs = tmp_path / "docs"
    docs.mkdir()

    (docs / "security.md").write_text(
        (
            "# Agent Security\n"
            "Multi-agent task orchestration requires "
            "dependency management, permission checks, "
            "and authorization validation.\n"
        ),
        encoding="utf-8",
    )

    settings = load_settings(
        provider_override="mock"
    )

    report = asyncio.run(
        run_crew(
            objective=(
                "Analyze multi-agent orchestration "
                "and authorization"
            ),
            settings=settings,
            docs_dir=docs,
        )
    )

    assert report.status == "completed"
    assert report.task_states["research"] == (
        TaskStatus.COMPLETED
    )
    assert report.task_states["review"] == (
        TaskStatus.COMPLETED
    )
    assert report.task_states["synthesis"] == (
        TaskStatus.COMPLETED
    )
    assert "Research Report" in report.final_output
    assert report.metrics["task_completion_rate"] == 1.0


def test_missing_evidence_returns_partial(tmp_path):
    settings = load_settings(
        provider_override="mock"
    )

    report = asyncio.run(
        run_crew(
            objective="Research unavailable sources",
            settings=settings,
            docs_dir=tmp_path / "missing",
        )
    )

    assert report.status == "partial"
    assert report.task_states["research"] == (
        TaskStatus.FAILED
    )
    assert report.task_states["review"] == (
        TaskStatus.BLOCKED
    )
    assert report.task_states["synthesis"] == (
        TaskStatus.BLOCKED
    )
