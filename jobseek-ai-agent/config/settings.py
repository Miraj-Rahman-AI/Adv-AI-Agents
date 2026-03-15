from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv


def _str_to_bool(value: str | None, default: bool = False) -> bool:
    """Convert environment string values to boolean."""
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass
class Settings:
    """
    Central configuration object for JobSeek AI Agent.

    Loads runtime settings from environment variables and exposes them
    as a typed configuration object for the rest of the system.
    """

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.2

    # Search / runtime
    target_job_count: int = 50
    max_iterations: int = 10
    request_timeout: int = 20
    headless: bool = True
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    )

    # Files / directories
    base_dir: Path = field(default_factory=lambda: Path(__file__).resolve().parents[1])
    data_dir: Path = field(init=False)
    raw_data_dir: Path = field(init=False)
    processed_data_dir: Path = field(init=False)
    output_dir: Path = field(init=False)
    output_json: Path = field(init=False)
    output_csv: Path = field(init=False)
    output_report: Path = field(init=False)

    # Site toggles
    enabled_sites: Dict[str, bool] = field(default_factory=dict)

    # Pipeline behavior
    enable_llm_filtering: bool = True
    enable_skill_extraction: bool = True
    enable_deduplication: bool = True
    save_raw_results: bool = True
    verbose: bool = True

    def __post_init__(self) -> None:
        self.data_dir = self.base_dir / "data"
        self.raw_data_dir = self.data_dir / "raw"
        self.processed_data_dir = self.data_dir / "processed"
        self.output_dir = self.base_dir / "output"
        self.output_json = self.output_dir / "jobs.json"
        self.output_csv = self.output_dir / "jobs.csv"
        self.output_report = self.output_dir / "report.md"

    @classmethod
    def from_env(cls, env_file: str | None = ".env") -> "Settings":
        """
        Load settings from the provided .env file and environment variables.
        """
        load_dotenv(env_file)

        settings = cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            openai_temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.2")),
            target_job_count=int(os.getenv("TARGET_JOB_COUNT", "50")),
            max_iterations=int(os.getenv("MAX_ITERATIONS", "10")),
            request_timeout=int(os.getenv("REQUEST_TIMEOUT", "20")),
            headless=_str_to_bool(os.getenv("HEADLESS", "true"), default=True),
            user_agent=os.getenv(
                "USER_AGENT",
                (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/127.0.0.0 Safari/537.36"
                ),
            ),
            enable_llm_filtering=_str_to_bool(
                os.getenv("ENABLE_LLM_FILTERING", "true"), default=True
            ),
            enable_skill_extraction=_str_to_bool(
                os.getenv("ENABLE_SKILL_EXTRACTION", "true"), default=True
            ),
            enable_deduplication=_str_to_bool(
                os.getenv("ENABLE_DEDUPLICATION", "true"), default=True
            ),
            save_raw_results=_str_to_bool(
                os.getenv("SAVE_RAW_RESULTS", "true"), default=True
            ),
            verbose=_str_to_bool(os.getenv("VERBOSE", "true"), default=True),
        )

        settings.enabled_sites = {
            "linkedin": _str_to_bool(os.getenv("ENABLE_LINKEDIN", "false")),
            "indeed": _str_to_bool(os.getenv("ENABLE_INDEED", "true")),
            "lagou": _str_to_bool(os.getenv("ENABLE_LAGOU", "true")),
            "zhipin": _str_to_bool(os.getenv("ENABLE_ZHIPIN", "true")),
            "liepin": _str_to_bool(os.getenv("ENABLE_LIEPIN", "true")),
        }

        return settings

    def ensure_directories(self) -> None:
        """
        Create all required directories for data and outputs.
        """
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)
        self.processed_data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def validate(self) -> None:
        """
        Validate critical settings. Raise ValueError on invalid configuration.
        """
        if self.target_job_count <= 0:
            raise ValueError("target_job_count must be greater than 0.")

        if self.max_iterations <= 0:
            raise ValueError("max_iterations must be greater than 0.")

        if self.request_timeout <= 0:
            raise ValueError("request_timeout must be greater than 0.")

        if not self.openai_model:
            raise ValueError("openai_model cannot be empty.")

    def to_dict(self) -> dict:
        """
        Convert settings to a serializable dictionary for logging/debugging.
        """
        return {
            "openai_model": self.openai_model,
            "openai_temperature": self.openai_temperature,
            "target_job_count": self.target_job_count,
            "max_iterations": self.max_iterations,
            "request_timeout": self.request_timeout,
            "headless": self.headless,
            "user_agent": self.user_agent,
            "data_dir": str(self.data_dir),
            "raw_data_dir": str(self.raw_data_dir),
            "processed_data_dir": str(self.processed_data_dir),
            "output_dir": str(self.output_dir),
            "output_json": str(self.output_json),
            "output_csv": str(self.output_csv),
            "output_report": str(self.output_report),
            "enabled_sites": self.enabled_sites,
            "enable_llm_filtering": self.enable_llm_filtering,
            "enable_skill_extraction": self.enable_skill_extraction,
            "enable_deduplication": self.enable_deduplication,
            "save_raw_results": self.save_raw_results,
            "verbose": self.verbose,
        }


settings = Settings.from_env()
