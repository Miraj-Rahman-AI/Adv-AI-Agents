from __future__ import annotations

import re
from typing import Any, Dict, List


class JobNormalizer:
    """
    Normalize job records into a consistent canonical format.
    """

    @staticmethod
    def normalize_job(job: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize all standard job fields.
        """
        normalized = {
            "title": JobNormalizer.normalize_text(job.get("title", "")),
            "company": JobNormalizer.normalize_text(job.get("company", "")),
            "location": JobNormalizer.normalize_text(job.get("location", "")),
            "salary": JobNormalizer.normalize_salary(job.get("salary", "")),
            "tech_tags": JobNormalizer.normalize_tech_tags(job.get("tech_tags", [])),
            "requirements": JobNormalizer.normalize_text(job.get("requirements", "")),
            "description": JobNormalizer.normalize_text(job.get("description", "")),
            "source": JobNormalizer.normalize_source(job.get("source", "")),
            "job_url": JobNormalizer.normalize_url(job.get("job_url", "")),
            "classification_reason": JobNormalizer.normalize_text(job.get("classification_reason", "")),
            "is_target_role": bool(job.get("is_target_role", False)),
        }
        return normalized

    @staticmethod
    def normalize_text(value: Any) -> str:
        """
        Clean whitespace and convert to string.
        """
        if value is None:
            return ""
        text = str(value)
        return " ".join(text.split()).strip()

    @staticmethod
    def normalize_salary(value: Any) -> str:
        """
        Normalize salary expressions.
        """
        text = JobNormalizer.normalize_text(value)
        text = text.replace("～", "-").replace("—", "-").replace("–", "-").replace("至", "-").replace("~", "-")
        text = re.sub(r"\s*-\s*", "-", text)
        return text

    @staticmethod
    def normalize_tech_tags(value: Any) -> List[str]:
        """
        Normalize and deduplicate tech tags.
        """
        if not isinstance(value, list):
            return []

        cleaned: List[str] = []
        for item in value:
            if item is None:
                continue
            tag = JobNormalizer.normalize_text(item)
            if tag and tag not in cleaned:
                cleaned.append(tag)

        return cleaned

    @staticmethod
    def normalize_source(value: Any) -> str:
        """
        Normalize source platform.
        """
        return JobNormalizer.normalize_text(value).lower()

    @staticmethod
    def normalize_url(value: Any) -> str:
        """
        Normalize URL string.
        """
        url = JobNormalizer.normalize_text(value)
        return url

    @staticmethod
    def normalize_jobs(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Normalize a list of job records.
        """
        return [JobNormalizer.normalize_job(job) for job in jobs]
