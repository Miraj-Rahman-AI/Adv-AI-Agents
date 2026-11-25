
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class Settings:
    project_root: Path
    provider: str
    model: str
    base_url: str
    api_key: str
    llm_timeout: float
    max_tokens: int
    max_concurrency: int
    max_retries: int
    max_tasks: int
    task_timeout: float
    workspace: Path
    agents: dict[str, Any] = field(default_factory=dict)
    tools: dict[str, Any] = field(default_factory=dict)


def read_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Required configuration file not found: {path}"
        )

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML mapping: {path}")

    return data


def load_settings(
    project_root: Path | None = None,
    provider_override: str | None = None,
) -> Settings:
    root = (project_root or PROJECT_ROOT).resolve()

    load_dotenv(root / ".env", override=False)

    orchestration = read_yaml(
        root / "configs" / "orchestration.yaml"
    ).get("orchestration", {})

    agents = read_yaml(
        root / "configs" / "agents.yaml"
    ).get("agents", {})

    tools = read_yaml(
        root / "configs" / "tools.yaml"
    ).get("tools", {})

    provider = (
        provider_override
        or os.getenv("LLM_PROVIDER", "mock")
    ).lower()

    if provider not in {"mock", "openai", "ollama"}:
        raise ValueError(f"Unsupported provider: {provider}")

    if provider == "ollama":
        model = os.getenv("OLLAMA_MODEL", "qwen3:8b")
        base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434/v1",
        )
        api_key = "ollama"
    else:
        model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        base_url = os.getenv(
            "OPENAI_BASE_URL",
            "https://api.openai.com/v1",
        )
        api_key = os.getenv("OPENAI_API_KEY", "")

    workspace_value = Path(
        os.getenv("WORKSPACE_PATH", ".")
    )

    workspace = (
        workspace_value
        if workspace_value.is_absolute()
        else root / workspace_value
    ).resolve()

    return Settings(
        project_root=root,
        provider=provider,
        model=model,
        base_url=base_url,
        api_key=api_key,
        llm_timeout=float(os.getenv("LLM_TIMEOUT", "60")),
        max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2000")),
        max_concurrency=int(
            os.getenv(
                "MAX_CONCURRENCY",
                str(orchestration.get("max_concurrency", 3)),
            )
        ),
        max_retries=int(
            os.getenv(
                "MAX_RETRIES",
                str(orchestration.get("max_retries", 1)),
            )
        ),
        max_tasks=int(
            os.getenv(
                "MAX_TASKS",
                str(orchestration.get("max_tasks", 12)),
            )
        ),
        task_timeout=float(
            orchestration.get("task_timeout_seconds", 120)
        ),
        workspace=workspace,
        agents=agents,
        tools=tools,
    )
