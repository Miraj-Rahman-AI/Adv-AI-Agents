from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


def load_settings() -> dict[str, Any]:
    """Load runtime settings from environment variables."""
    load_dotenv()

    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "openai_temperature": float(os.getenv("OPENAI_TEMPERATURE", "0.2")),
        "target_job_count": int(os.getenv("TARGET_JOB_COUNT", "50")),
        "max_iterations": int(os.getenv("MAX_ITERATIONS", "10")),
        "request_timeout": int(os.getenv("REQUEST_TIMEOUT", "20")),
        "output_json": os.getenv("OUTPUT_JSON", "output/jobs.json"),
        "output_csv": os.getenv("OUTPUT_CSV", "output/jobs.csv"),
        "user_agent": os.getenv(
            "USER_AGENT",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        ),
        "headless": os.getenv("HEADLESS", "true").lower() == "true",
        "enabled_sites": {
            "linkedin": os.getenv("ENABLE_LINKEDIN", "false").lower() == "true",
            "indeed": os.getenv("ENABLE_INDEED", "true").lower() == "true",
            "lagou": os.getenv("ENABLE_LAGOU", "true").lower() == "true",
            "zhipin": os.getenv("ENABLE_ZHIPIN", "true").lower() == "true",
            "liepin": os.getenv("ENABLE_LIEPIN", "true").lower() == "true",
        },
    }


def ensure_output_dirs(settings: dict[str, Any]) -> None:
    """Create output directories if they do not exist."""
    Path(settings["output_json"]).parent.mkdir(parents=True, exist_ok=True)
    Path(settings["output_csv"]).parent.mkdir(parents=True, exist_ok=True)


def run_pipeline(settings: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Placeholder pipeline runner.

    Replace this with your actual orchestrator later, for example:
        from pipeline.orchestrator import run_jobseek_agent
        return run_jobseek_agent(settings)
    """
    print("[INFO] Starting JobSeek AI Agent...")
    print(f"[INFO] Target job count: {settings['target_job_count']}")
    print(f"[INFO] Max iterations: {settings['max_iterations']}")
    print(f"[INFO] Model: {settings['openai_model']}")
    print(f"[INFO] Enabled sites: {settings['enabled_sites']}")

    # Demo sample output so the project can run end-to-end initially
    sample_jobs = [
        {
            "title": "AI Engineer Intern",
            "company": "Example Tech",
            "location": "Beijing",
            "salary": "15K-20K",
            "tech_tags": ["Python", "PyTorch", "LLM"],
            "requirements": "Experience with machine learning, NLP, and model deployment.",
            "source": "Indeed",
            "job_url": "https://example.com/job/1",
        },
        {
            "title": "Machine Learning Engineer",
            "company": "Demo AI Lab",
            "location": "Shanghai",
            "salary": "20K-30K",
            "tech_tags": ["TensorFlow", "Computer Vision", "Deep Learning"],
            "requirements": "Familiar with deep learning frameworks and data pipelines.",
            "source": "Lagou",
            "job_url": "https://example.com/job/2",
        },
    ]

    return sample_jobs


def export_json(data: list[dict[str, Any]], output_path: str) -> None:
    """Save results to JSON."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def export_csv(data: list[dict[str, Any]], output_path: str) -> None:
    """Save results to CSV."""
    try:
        import pandas as pd
    except ImportError as exc:
        raise RuntimeError(
            "pandas is required to export CSV. Install dependencies from requirements.txt."
        ) from exc

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")


def main() -> None:
    """Main entry point."""
    settings = load_settings()

    if not settings["openai_api_key"]:
        print("[WARNING] OPENAI_API_KEY is not set. LLM-based features may not work.")

    ensure_output_dirs(settings)

    jobs = run_pipeline(settings)

    export_json(jobs, settings["output_json"])
    export_csv(jobs, settings["output_csv"])

    print(f"[INFO] Exported JSON to: {settings['output_json']}")
    print(f"[INFO] Exported CSV to: {settings['output_csv']}")
    print(f"[INFO] Total jobs collected: {len(jobs)}")


if __name__ == "__main__":
    main()
