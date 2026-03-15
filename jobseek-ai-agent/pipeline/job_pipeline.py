from __future__ import annotations

from typing import Any, Dict, List

from agents import ClassifierAgent, QueryRewriterAgent, SkillExtractorAgent
from config.settings import Settings
from pipeline.state import PipelineState
from tools import ExporterTool, ParserTool


class JobPipeline:
    """
    Core data-processing pipeline for job records.

    Responsibilities:
    - parse raw job pages or raw job dicts
    - classify target AI roles
    - enrich jobs with skills
    - deduplicate
    - select final results
    - export outputs
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.parser = ParserTool()
        self.classifier = ClassifierAgent(settings)
        self.skill_extractor = SkillExtractorAgent(settings)
        self.query_rewriter = QueryRewriterAgent(settings)
        self.exporter = ExporterTool(settings)

    def process_jobs(self, state: PipelineState) -> List[Dict[str, Any]]:
        """
        Process all raw jobs in state and produce final jobs.
        """
        processed_jobs: List[Dict[str, Any]] = []

        for raw_job in state.raw_jobs:
            normalized = self.parser.parse_raw_job_record(raw_job)

            is_target, reason = self.classifier.classify(normalized)
            state.log(
                f"[CLASSIFY] title='{normalized.get('title', '')}' "
                f"| keep={is_target} | reason={reason}"
            )

            if not is_target:
                continue

            enriched = self.skill_extractor.enrich_job(normalized)
            processed_jobs.append(enriched)

        deduped = self.deduplicate_jobs(processed_jobs)
        final_jobs = deduped[: self.settings.target_job_count]

        state.processed_jobs = processed_jobs
        state.set_final_jobs(final_jobs)

        return final_jobs

    def parse_pages_to_jobs(self, pages: List[Dict[str, Any]], state: PipelineState) -> List[Dict[str, Any]]:
        """
        Convert scraped pages into raw structured jobs.
        """
        parsed_jobs: List[Dict[str, Any]] = []

        for page in pages:
            try:
                job = self.parser.parse_job_page(page, source=page.get("source", ""))
                parsed_jobs.append(job)
                state.log(
                    f"[PARSE] Parsed job from url={page.get('url', '')} "
                    f"title='{job.get('title', '')}'"
                )
            except Exception as exc:
                state.add_error(f"[PARSE_ERROR] url={page.get('url', '')} | error={exc}")

        return parsed_jobs

    @staticmethod
    def deduplicate_jobs(jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Simple deduplication using:
        - job_url if available
        - otherwise title + company + location signature
        """
        seen = set()
        deduped: List[Dict[str, Any]] = []

        for job in jobs:
            key = JobPipeline._job_key(job)
            if key in seen:
                continue
            seen.add(key)
            deduped.append(job)

        return deduped

    @staticmethod
    def _job_key(job: Dict[str, Any]) -> str:
        """
        Build a stable deduplication key for a job.
        """
        url = str(job.get("job_url", "")).strip().lower()
        if url:
            return f"url::{url}"

        title = str(job.get("title", "")).strip().lower()
        company = str(job.get("company", "")).strip().lower()
        location = str(job.get("location", "")).strip().lower()

        return f"sig::{title}::{company}::{location}"

    def export_results(self, jobs: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Export final jobs to JSON / CSV / Markdown report.
        """
        json_path = self.exporter.export_json(jobs)
        csv_path = self.exporter.export_csv(jobs)
        report_path = self.exporter.export_report(jobs)

        return {
            "json": str(json_path),
            "csv": str(csv_path),
            "report": str(report_path),
        }
