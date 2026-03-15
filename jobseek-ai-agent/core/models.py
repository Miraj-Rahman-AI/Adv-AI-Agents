from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List


@dataclass
class JobRecord:
    """
    Core internal job model used across the pipeline.
    """

    title: str = ""
    company: str = ""
    location: str = ""
    salary: str = ""
    tech_tags: List[str] = field(default_factory=list)
    requirements: str = ""
    description: str = ""
    source: str = ""
    job_url: str = ""

    classification_reason: str = ""
    is_target_role: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "JobRecord":
        """Create model from dictionary."""
        return cls(
            title=str(data.get("title", "")),
            company=str(data.get("company", "")),
            location=str(data.get("location", "")),
            salary=str(data.get("salary", "")),
            tech_tags=list(data.get("tech_tags", [])) if isinstance(data.get("tech_tags"), list) else [],
            requirements=str(data.get("requirements", "")),
            description=str(data.get("description", "")),
            source=str(data.get("source", "")),
            job_url=str(data.get("job_url", "")),
            classification_reason=str(data.get("classification_reason", "")),
            is_target_role=bool(data.get("is_target_role", False)),
            metadata=data.get("metadata", {}) if isinstance(data.get("metadata", {}), dict) else {},
        )


@dataclass
class SearchQueryRecord:
    """
    Track a query and its execution outcome.
    """

    query: str
    source: str
    page: int = 1
    success: bool = False
    result_count: int = 0
    error_message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PipelineReport:
    """
    Summary object for reporting pipeline execution.
    """

    goal: str
    target_job_count: int
    collected_job_count: int
    processed_job_count: int
    final_job_count: int
    iterations_used: int
    sources_used: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
