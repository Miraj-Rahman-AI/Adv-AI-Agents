
from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from agentcrew.agents import (
    AnalystAgent,
    CoordinatorAgent,
    ExecutionAgent,
    PlannerAgent,
    ResearchAgent,
    ReviewerAgent,
    SynthesisAgent,
)
from agentcrew.communication import MessageBus
from agentcrew.config import Settings, load_settings
from agentcrew.llm import build_llm_client
from agentcrew.models import ExecutionReport
from agentcrew.observability import TraceRecorder
from agentcrew.orchestration import AgentCrewWorkflow
from agentcrew.security import (
    AuthorizationContext,
    PolicyEngine,
)
from agentcrew.tools import (
    ToolExecutor,
    build_default_registry,
    load_documents,
)


async def run_crew(
    objective: str,
    settings: Settings | None = None,
    docs_dir: Path | None = None,
    tracer: TraceRecorder | None = None,
) -> ExecutionReport:
    settings = settings or load_settings()

    tracer = tracer or TraceRecorder()
    message_bus = MessageBus()

    document_directory = (
        docs_dir
        if docs_dir is not None
        else settings.project_root / "docs"
    )

    documents = load_documents(
        document_directory
    )

    llm = build_llm_client(settings)

    registry = build_default_registry(
        documents=documents
    )

    policy = PolicyEngine(
        agent_rules=settings.agents,
        tool_rules=settings.tools,
    )

    # This example application explicitly authorizes
    # local document retrieval and arithmetic only.
    authorization = AuthorizationContext(
        allowed_tools=frozenset({
            "document_search",
            "calculator",
        }),
        allowed_actions=frozenset({
            "read",
            "compute",
        }),
        allowed_resources=frozenset({
            "documents",
            "numbers",
        }),
    )

    tools = ToolExecutor(
        registry=registry,
        policy=policy,
        authorization=authorization,
        tracer=tracer,
    )

    agents = {
        "coordinator": CoordinatorAgent(llm),
        "planner": PlannerAgent(llm),
        "researcher": ResearchAgent(llm, tools),
        "executor": ExecutionAgent(llm, tools),
        "analyst": AnalystAgent(llm),
        "reviewer": ReviewerAgent(llm),
        "synthesizer": SynthesisAgent(llm),
    }

    workflow = AgentCrewWorkflow(
        agents=agents,
        settings=settings,
        message_bus=message_bus,
        tracer=tracer,
    )

    return await workflow.run(objective)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="agentcrew",
        description=(
            "AgentCrew-AI multi-agent execution CLI"
        ),
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    run_parser = subparsers.add_parser(
        "run",
        help="Execute a collaborative agent workflow",
    )

    run_parser.add_argument(
        "--task",
        required=True,
        help="User objective to complete",
    )

    run_parser.add_argument(
        "--provider",
        choices=["mock", "openai", "ollama"],
        default=None,
    )

    run_parser.add_argument(
        "--docs-dir",
        type=Path,
        default=None,
        help="Directory of approved local Markdown documents",
    )

    run_parser.add_argument(
        "--json",
        action="store_true",
        help="Print full execution report as JSON",
    )

    run_parser.add_argument(
        "--trace-path",
        type=Path,
        default=None,
        help="Optional JSONL trace output path",
    )

    args = parser.parse_args(argv)

    try:
        settings = load_settings(
            provider_override=args.provider
        )

        tracer = TraceRecorder()

        report = asyncio.run(
            run_crew(
                objective=args.task,
                settings=settings,
                docs_dir=args.docs_dir,
                tracer=tracer,
            )
        )

        if args.trace_path is not None:
            tracer.export_jsonl(args.trace_path)

        if args.json:
            print(
                json.dumps(
                    report.to_dict(),
                    indent=2,
                    ensure_ascii=False,
                )
            )
        else:
            print("\n" + "=" * 60)
            print("AgentCrew-AI Execution Report")
            print("=" * 60)

            print(f"\nStatus: {report.status}")
            print(
                f"Duration: "
                f"{report.duration_seconds:.2f}s"
            )

            print("\nFinal Output:")
            print(report.final_output)

            if report.errors:
                print("\nErrors:")
                for error in report.errors:
                    print(f"- {error}")

            print("\nMetrics:")
            for key, value in report.metrics.items():
                print(f"  {key}: {value}")

        return (
            0
            if report.status == "completed"
            else 1
        )

    except Exception as error:
        print(
            f"AgentCrew-AI error: "
            f"{type(error).__name__}: {error}"
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
