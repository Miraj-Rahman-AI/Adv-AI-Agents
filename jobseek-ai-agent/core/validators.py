from __future__ import annotations

from typing import Any, Dict, List, Tuple

from config.constants import REQUIRED_JOB_FIELDS, SUPPORTED_SOURCES


class JobValidator:
    """
    Validate job records before they enter later pipeline stages.
    """

    @staticmethod
    def validate_required_fields(job: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Check whether required fields are present and non-empty.
        """
        errors: List[str] = []

        for field in REQUIRED_JOB_FIELDS:
            value = job.get(field, "")
            if not isinstance(value, str) or not value.strip():
                errors.append(f"Missing required field: {field}")

        return len(errors) == 0, errors

    @staticmethod
    def validate_source(job: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate source platform.
        """
        source = str(job.get("source", "")).strip().lower()
        if not source:
            return False, "Missing source field."

        if source not in SUPPORTED_SOURCES:
            return False, f"Unsupported source: {source}"

        return True, ""

    @staticmethod
    def validate_tech_tags(job: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate tech_tags field format.
        """
        tech_tags = job.get("tech_tags", [])
        if not isinstance(tech_tags, list):
            return False, "tech_tags must be a list."

        for tag in tech_tags:
            if not isinstance(tag, str):
                return False, "Each tech tag must be a string."

        return True, ""

    @staticmethod
    def validate_job(job: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Run all validations for a job record.
        """
        errors: List[str] = []

        ok_required, required_errors = JobValidator.validate_required_fields(job)
        if not ok_required:
            errors.extend(required_errors)

        ok_source, source_error = JobValidator.validate_source(job)
        if not ok_source:
            errors.append(source_error)

        ok_tags, tags_error = JobValidator.validate_tech_tags(job)
        if not ok_tags:
            errors.append(tags_error)

        return len(errors) == 0, errors
