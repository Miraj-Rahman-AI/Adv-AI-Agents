from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple


class Deduplicator:
    """
    Remove duplicate or near-duplicate job records.
    """

    @staticmethod
    def deduplicate(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicate using a stable key:
        1. job_url if present
        2. fallback to title + company + location
        """
        seen: Set[str] = set()
        deduped: List[Dict[str, Any]] = []

        for job in jobs:
            key = Deduplicator.build_key(job)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(job)

        return deduped

    @staticmethod
    def build_key(job: Dict[str, Any]) -> str:
        """
        Build a unique key for deduplication.
        """
        url = str(job.get("job_url", "")).strip().lower()
        if url:
            return f"url::{url}"

        title = str(job.get("title", "")).strip().lower()
        company = str(job.get("company", "")).strip().lower()
        location = str(job.get("location", "")).strip().lower()

        return f"sig::{title}::{company}::{location}"

    @staticmethod
    def find_duplicates(jobs: List[Dict[str, Any]]) -> List[Tuple[int, int]]:
        """
        Return duplicate index pairs for debugging.
        """
        key_to_index: Dict[str, int] = {}
        duplicates: List[Tuple[int, int]] = []

        for idx, job in enumerate(jobs):
            key = Deduplicator.build_key(job)
            if key in key_to_index:
                duplicates.append((key_to_index[key], idx))
            else:
                key_to_index[key] = idx

        return duplicates
