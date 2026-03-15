from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class JobSchema(BaseModel):
    """
    Canonical schema for a structured job record.
    """

    title: str = Field(default="", description="Job title")
    company: str = Field(default="", description="Company name")
    location: str = Field(default="", description="Job location")
    salary: str = Field(default="", description="Salary range")
    tech_tags: List[str] = Field(default_factory=list, description="Technical tags")
    requirements: str = Field(default="", description="Core requirements summary")
    description: str = Field(default="", description="Full or partial job description")
    source: str = Field(default="", description="Recruitment platform source")
    job_url: str = Field(default="", description="Job posting URL")

    classification_reason: str = Field(default="", description="Why the job was classified as target/non-target")
    is_target_role: bool = Field(default=False, description="Whether the job matches AI target role")

    @field_validator("tech_tags")
    @classmethod
    def validate_tech_tags(cls, value: List[str]) -> List[str]:
        cleaned = []
        for item in value:
            if not isinstance(item, str):
                continue
            tag = " ".join(item.split()).strip()
            if tag and tag not in cleaned:
                cleaned.append(tag)
        return cleaned

    @field_validator("title", "company", "location", "salary", "requirements", "description", "source", "job_url")
    @classmethod
    def normalize_text_fields(cls, value: str) -> str:
        if not isinstance(value, str):
            return ""
        return " ".join(value.split()).strip()


class SearchPageSchema(BaseModel):
    """
    Schema for a fetched page before parsing.
    """

    url: str = Field(default="")
    title: str = Field(default="")
    text: str = Field(default="")
    html: str = Field(default="")
    source: str = Field(default="")


class SearchTaskSchema(BaseModel):
    """
    Schema for a search task.
    """

    query: str
    source: str
    page: int = 1


class ExportSummarySchema(BaseModel):
    """
    Schema for exported result summary.
    """

    total_jobs: int = 0
    unique_sources: List[str] = Field(default_factory=list)
    unique_locations: List[str] = Field(default_factory=list)
    output_json_path: Optional[str] = None
    output_csv_path: Optional[str] = None
    output_report_path: Optional[str] = None
