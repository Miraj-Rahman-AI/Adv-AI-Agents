from __future__ import annotations

import json
import sys
from pathlib import Path

# Make project root importable when running this file directly
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from config.settings import settings
from pipeline import run_jobseek_agent


def print_banner() -> None:
    print("=" * 70)
    print("JobSeek AI Agent - Demo Run")
    print("=" * 70)


def print_summary(state) -> None:
    summary = state.summary()

    print("\n[SUMMARY]")
    for key, value in summary.items():
        print(f"- {key}: {value}")

    print("\n[FINAL JOBS]")
    if not state.final_jobs:
        print("No jobs collected.")
        return

    for idx, job in enumerate(state.final_jobs[:10], start=1):
        print(
            f"{idx}. {job.get('title', '')} | "
            f"{job.get('company', '')} | "
            f"{job.get('location', '')} | "
            f"{job.get('source', '')}"
        )

    if state.errors:
        print("\n[ERRORS]")
        for err in state.errors[:10]:
            print(f"- {err}")

    print("\n[RECENT LOGS]")
    for log in state.logs[-10:]:
        print(f"- {log}")


def save_demo_output(state) -> Path:
    output_path = PROJECT_ROOT / "examples" / "example_output.json"

    payload = {
        "summary": state.summary(),
        "final_jobs": state.final_jobs,
        "errors": state.errors,
        "logs": state.logs[-20:],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return output_path


def main() -> None:
    print_banner()

    settings.ensure_directories()
    settings.validate()

    goal = "Find 10 AI Engineer internship or campus recruitment jobs"

    print(f"[INFO] Goal: {goal}")
    print(f"[INFO] Enabled sources: {settings.enabled_sites}")
    print(f"[INFO] Model: {settings.openai_model}")

    state = run_jobseek_agent(settings, goal)

    print_summary(state)

    saved_path = save_demo_output(state)
    print(f"\n[INFO] Demo output saved to: {saved_path}")


if __name__ == "__main__":
    main()
