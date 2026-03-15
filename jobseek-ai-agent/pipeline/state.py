from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Set


@dataclass
class PipelineState:
    """
    Runtime state container for the JobSeek AI Agent pipeline.

    This object tracks:
    - original goal
    - active / attempted queries
    - collected raw and processed jobs
    - visited URLs
    - iteration progress
    - execution logs
    """

    goal: str
    target_job_count: int
    max_iterations: int

    current_iteration: int = 0

    initial_queries: List[str] = field(default_factory=list)
    active_queries: List[str] = field(default_factory=list)
    attempted_queries: List[str] = field(default_factory=list)

    search_tasks: List[Dict[str, Any]] = field(default_factory=list)
    visited_urls: Set[str] = field(default_factory=set)

    raw_pages: List[Dict[str, Any]] = field(default_factory=list)
    raw_jobs: List[Dict[str, Any]] = field(default_factory=list)
    processed_jobs: List[Dict[str, Any]] = field(default_factory=list)
    final_jobs: List[Dict[str, Any]] = field(default_factory=list)

    errors: List[str] = field(default_factory=list)
    logs: List[str] = field(default_factory=list)

    def log(self, message: str) -> None:
        """Append a pipeline log message."""
        self.logs.append(message)

    def add_error(self, message: str) -> None:
        """Append an error message."""
        self.errors.append(message)

    def mark_query_attempted(self, query: str) -> None:
        """Track queries that have already been used."""
        if query not in self.attempted_queries:
            self.attempted_queries.append(query)

    def add_search_task(self, task: Dict[str, Any]) -> None:
        """Add a search task if not already present."""
        if task not in self.search_tasks:
            self.search_tasks.append(task)

    def add_page(self, page: Dict[str, Any]) -> None:
        """Add a raw page record."""
        self.raw_pages.append(page)

    def add_raw_job(self, job: Dict[str, Any]) -> None:
        """Add a raw parsed job."""
        self.raw_jobs.append(job)

    def add_processed_job(self, job: Dict[str, Any]) -> None:
        """Add a processed / enriched job."""
        self.processed_jobs.append(job)

    def set_final_jobs(self, jobs: List[Dict[str, Any]]) -> None:
        """Set final output jobs."""
        self.final_jobs = jobs

    def should_stop(self) -> bool:
        """
        Stop if target reached or iteration budget exhausted.
        """
        if len(self.final_jobs) >= self.target_job_count:
            return True

        if self.current_iteration >= self.max_iterations:
            return True

        return False

    def next_iteration(self) -> None:
        """Advance iteration counter."""
        self.current_iteration += 1

    def summary(self) -> Dict[str, Any]:
        """Return a compact summary for debugging or reporting."""
        return {
            "goal": self.goal,
            "target_job_count": self.target_job_count,
            "max_iterations": self.max_iterations,
            "current_iteration": self.current_iteration,
            "initial_queries": self.initial_queries,
            "active_queries_count": len(self.active_queries),
            "attempted_queries_count": len(self.attempted_queries),
            "search_tasks_count": len(self.search_tasks),
            "visited_urls_count": len(self.visited_urls),
            "raw_pages_count": len(self.raw_pages),
            "raw_jobs_count": len(self.raw_jobs),
            "processed_jobs_count": len(self.processed_jobs),
            "final_jobs_count": len(self.final_jobs),
            "errors_count": len(self.errors),
            "logs_count": len(self.logs),
        }
