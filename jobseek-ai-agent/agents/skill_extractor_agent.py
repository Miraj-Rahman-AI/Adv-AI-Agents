from __future__ import annotations

from typing import Any, Dict, List

from config.constants import TECH_TAG_VOCAB
from config.settings import Settings


class SkillExtractorAgent:
    """
    Extract technical skills / tech tags from a job posting.

    This starter implementation uses vocabulary matching.
    Later you can replace it with LLM-based extraction.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def extract_skills(self, job: Dict[str, Any]) -> List[str]:
        """
        Extract known technical tags from title / description / requirements.
        """
        text = self._compose_text(job)
        found_tags = []

        for tag in TECH_TAG_VOCAB:
            if tag.lower() in text and tag not in found_tags:
                found_tags.append(tag)

        return found_tags

    def enrich_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add tech_tags field to a job if missing or incomplete.
        """
        extracted = self.extract_skills(job)

        existing_tags = job.get("tech_tags", [])
        if not isinstance(existing_tags, list):
            existing_tags = []

        merged = []
        for tag in existing_tags + extracted:
            if tag not in merged:
                merged.append(tag)

        job["tech_tags"] = merged
        return job

    @staticmethod
    def _compose_text(job: Dict[str, Any]) -> str:
        """
        Build lowercase searchable text from job record.
        """
        return " ".join(
            [
                str(job.get("title", "")),
                str(job.get("requirements", "")),
                str(job.get("description", "")),
            ]
        ).lower()
