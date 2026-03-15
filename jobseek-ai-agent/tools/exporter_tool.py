from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

from config.settings import Settings


class ExporterTool:
    """
    Export tool for saving job data into JSON, CSV, and Markdown report formats.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def export_json(self, data: List[Dict[str, Any]], output_path: str | Path | None = None) -> Path:
        """
        Export structured job data to JSON.
        """
        path = Path(output_path) if output_path else self.settings.output_json
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        return path

    def export_csv(self, data: List[Dict[str, Any]], output_path: str | Path | None = None) -> Path:
        """
        Export structured job data to CSV.
        """
        path = Path(output_path) if output_path else self.settings.output_csv
        path.parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(data)
        df.to_csv(path, index=False, encoding="utf-8-sig")

        return path

    def export_report(self, data: List[Dict[str, Any]], output_path: str | Path | None = None) -> Path:
        """
        Export a simple Markdown summary report.
        """
        path = Path(output_path) if output_path else self.settings.output_report
        path.parent.mkdir(parents=True, exist_ok=True)

        report = self._build_markdown_report(data)

        with open(path, "w", encoding="utf-8") as f:
            f.write(report)

        return path

    @staticmethod
    def _build_markdown_report(data: List[Dict[str, Any]]) -> str:
        """
        Build a concise Markdown report from collected job data.
        """
        total_jobs = len(data)
        sources = sorted({job.get("source", "") for job in data if job.get("source")})
        locations = sorted({job.get("location", "") for job in data if job.get("location")})

        lines = [
            "# JobSeek AI Agent Report",
            "",
            f"- Total jobs collected: **{total_jobs}**",
            f"- Unique sources: **{len(sources)}**",
            f"- Sources: {', '.join(sources) if sources else 'N/A'}",
            f"- Locations covered: {', '.join(locations) if locations else 'N/A'}",
            "",
            "## Sample Jobs",
            "",
        ]

        for idx, job in enumerate(data[:10], start=1):
            lines.extend(
                [
                    f"### {idx}. {job.get('title', 'Unknown Title')}",
                    f"- Company: {job.get('company', '')}",
                    f"- Location: {job.get('location', '')}",
                    f"- Salary: {job.get('salary', '')}",
                    f"- Tech Tags: {', '.join(job.get('tech_tags', [])) if isinstance(job.get('tech_tags'), list) else ''}",
                    f"- Source: {job.get('source', '')}",
                    f"- URL: {job.get('job_url', '')}",
                    "",
                ]
            )

        return "\n".join(lines)
