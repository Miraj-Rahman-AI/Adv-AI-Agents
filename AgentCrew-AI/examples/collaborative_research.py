
from __future__ import annotations

import asyncio
from pathlib import Path

from agentcrew.config import load_settings
from agentcrew.main import run_crew


async def main() -> None:
    settings = load_settings(
        provider_override="mock"
    )

    docs_dir = (
        settings.project_root / "docs"
    )

    objective = (
        "Summarize the AgentCrew-AI multi-agent "
        "architecture, workflow orchestration, "
        "and security responsibilities."
    )

    report = await run_crew(
        objective=objective,
        settings=settings,
        docs_dir=docs_dir,
    )

    print("\n=== AgentCrew-AI ===")
    print(f"Status: {report.status}")

    print("\nFinal Report:")
    print(report.final_output)

    print("\nTask States:")
    for task_id, status in report.task_states.items():
        print(f"  {task_id}: {status.value}")

    print("\nMetrics:")
    for key, value in report.metrics.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(main())
