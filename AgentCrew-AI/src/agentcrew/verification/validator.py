
from __future__ import annotations

from typing import Any


def validate_research_evidence(
    results: dict[str, Any],
) -> list[str]:
    """Run deterministic evidence provenance checks."""

    issues = []

    research = results.get("research", {})
    output = research.get("output", {})

    sources = output.get("sources", [])
    findings = output.get("findings", [])

    if not isinstance(sources, list) or not sources:
        issues.append("Missing supporting research sources")
        return issues

    allowed_sources = {
        source.get("source")
        for source in sources
        if isinstance(source, dict)
    }

    if not isinstance(findings, list):
        issues.append("Research findings must be a list")
        return issues

    for finding in findings:
        if not isinstance(finding, dict):
            issues.append("Malformed research finding")
            continue

        if finding.get("source") not in allowed_sources:
            issues.append(
                "Research finding cites an unknown source"
            )

    return issues
